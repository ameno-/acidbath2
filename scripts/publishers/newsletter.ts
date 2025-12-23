/**
 * Newsletter Publisher - Multi-provider email newsletter distribution
 * Supports: Substack, Buttondown, Mailchimp
 */

import {
  Publisher,
  PublishResult,
  PlatformContent,
  PublisherOptions,
} from '../types/publisher.js';
import { BasePublisher } from './base-publisher.js';
import { promises as fs } from 'fs';
import * as path from 'path';

export class NewsletterPublisher extends BasePublisher implements Publisher {
  readonly platform = 'newsletter';

  constructor(options: PublisherOptions) {
    super(options, 'newsletter');
  }

  /**
   * Validate newsletter configuration
   */
  async validate(): Promise<boolean> {
    const provider = process.env.NEWSLETTER_PROVIDER?.toLowerCase();

    if (!provider) {
      this.logError('NEWSLETTER_PROVIDER environment variable is not set');
      return false;
    }

    if (!['substack', 'buttondown', 'mailchimp'].includes(provider)) {
      this.logError(
        `Invalid NEWSLETTER_PROVIDER: ${provider}. Must be one of: substack, buttondown, mailchimp`
      );
      return false;
    }

    // Validate provider-specific API keys
    const apiKeyMap: Record<string, string> = {
      substack: 'SUBSTACK_API_KEY',
      buttondown: 'BUTTONDOWN_API_KEY',
      mailchimp: 'MAILCHIMP_API_KEY',
    };

    const requiredKey = apiKeyMap[provider];
    if (!process.env[requiredKey]) {
      this.logError(`${requiredKey} environment variable is not set`);
      return false;
    }

    // Mailchimp requires additional configuration
    if (provider === 'mailchimp' && !process.env.MAILCHIMP_SERVER_PREFIX) {
      this.logError('MAILCHIMP_SERVER_PREFIX environment variable is not set');
      return false;
    }

    this.log(`Newsletter provider validated: ${provider}`);
    return true;
  }

  /**
   * Publish content to newsletter platform
   */
  protected async publishContent(content: PlatformContent): Promise<PublishResult> {
    try {
      const provider = process.env.NEWSLETTER_PROVIDER?.toLowerCase();

      if (!provider) {
        return {
          success: false,
          platform: this.platform,
          error: 'NEWSLETTER_PROVIDER not configured',
        };
      }

      // Route to provider-specific implementation
      switch (provider) {
        case 'buttondown':
          return await this.publishToButtondown(content);
        case 'substack':
          return await this.publishToSubstack(content);
        case 'mailchimp':
          return await this.publishToMailchimp(content);
        default:
          return {
            success: false,
            platform: this.platform,
            error: `Unknown provider: ${provider}`,
          };
      }
    } catch (error: any) {
      this.logError('Newsletter publish failed:', error);
      return {
        success: false,
        platform: this.platform,
        error: error.message || 'Unknown error',
      };
    }
  }

  /**
   * Publish to Buttondown
   * https://buttondown.email/api/documentation
   */
  private async publishToButtondown(content: PlatformContent): Promise<PublishResult> {
    try {
      this.log('Publishing to Buttondown...');

      const apiKey = process.env.BUTTONDOWN_API_KEY;
      if (!apiKey) {
        return {
          success: false,
          platform: this.platform,
          error: 'BUTTONDOWN_API_KEY not set',
        };
      }

      // Prepare email content
      const emailSubject = this.generateEmailSubject(content.title);
      const emailBody = this.formatEmailBody(content);

      // Buttondown API request
      const response = await this.fetch('https://api.buttondown.email/v1/emails', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          subject: emailSubject,
          body_html: emailBody,
          tags: content.tags,
          publish_immediately: false, // Draft by default for review
          metadata: {
            canonical_url: content.canonicalUrl,
            post_title: content.title,
            source: 'ACIDBATH',
          },
        }),
      });

      const data = await response.json();

      if (!data.id) {
        return {
          success: false,
          platform: this.platform,
          error: 'Failed to create Buttondown email: no ID returned',
        };
      }

      this.log(`Email created on Buttondown: ${data.id}`);

      return {
        success: true,
        platform: this.platform,
        url: `https://buttondown.email/emails/${data.id}`,
        metadata: {
          provider: 'buttondown',
          emailId: data.id,
          draft: true,
        },
      };
    } catch (error: any) {
      this.logError('Buttondown publish error:', error);
      return {
        success: false,
        platform: this.platform,
        error: error.message || 'Buttondown API error',
      };
    }
  }

  /**
   * Publish to Substack
   * https://substack.com/api/v1
   */
  private async publishToSubstack(content: PlatformContent): Promise<PublishResult> {
    try {
      this.log('Publishing to Substack...');

      const apiKey = process.env.SUBSTACK_API_KEY;
      if (!apiKey) {
        return {
          success: false,
          platform: this.platform,
          error: 'SUBSTACK_API_KEY not set',
        };
      }

      // Prepare email content
      const emailSubject = this.generateEmailSubject(content.title);
      const emailBody = this.formatEmailBody(content);

      // Substack API request
      const response = await this.fetch('https://api.substack.com/v1/drafts', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: emailSubject,
          body_html: emailBody,
          description: content.excerpt || content.title,
          canonical_url: content.canonicalUrl,
          subtitle: content.excerpt,
          byline_name: 'ACIDBATH',
          publish_on: null, // Save as draft
        }),
      });

      const data = await response.json();

      if (!data.id) {
        return {
          success: false,
          platform: this.platform,
          error: 'Failed to create Substack draft: no ID returned',
        };
      }

      this.log(`Draft created on Substack: ${data.id}`);

      return {
        success: true,
        platform: this.platform,
        url: `https://substack.com/i/${data.id}`,
        metadata: {
          provider: 'substack',
          draftId: data.id,
          draft: true,
        },
      };
    } catch (error: any) {
      this.logError('Substack publish error:', error);
      return {
        success: false,
        platform: this.platform,
        error: error.message || 'Substack API error',
      };
    }
  }

  /**
   * Publish to Mailchimp
   * https://mailchimp.com/developer/marketing/api/
   */
  private async publishToMailchimp(content: PlatformContent): Promise<PublishResult> {
    try {
      this.log('Publishing to Mailchimp...');

      const apiKey = process.env.MAILCHIMP_API_KEY;
      const serverPrefix = process.env.MAILCHIMP_SERVER_PREFIX;

      if (!apiKey || !serverPrefix) {
        return {
          success: false,
          platform: this.platform,
          error: 'MAILCHIMP_API_KEY or MAILCHIMP_SERVER_PREFIX not set',
        };
      }

      // Prepare email content
      const emailSubject = this.generateEmailSubject(content.title);
      const emailBody = this.formatEmailBody(content);

      // Step 1: Create campaign
      const campaignResponse = await this.fetch(
        `https://${serverPrefix}.api.mailchimp.com/3.0/campaigns`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            type: 'regular',
            recipients: {
              list_id: process.env.MAILCHIMP_LIST_ID || '',
            },
            settings: {
              subject_line: emailSubject,
              title: content.title,
              from_name: 'ACIDBATH',
              reply_to: process.env.MAILCHIMP_REPLY_TO || '',
            },
            tracking: {
              opens: true,
              html_clicks: true,
              text_clicks: false,
            },
          }),
        }
      );

      const campaignData = await campaignResponse.json();

      if (!campaignData.id) {
        return {
          success: false,
          platform: this.platform,
          error: 'Failed to create Mailchimp campaign: no ID returned',
        };
      }

      this.log(`Campaign created on Mailchimp: ${campaignData.id}`);

      // Step 2: Set campaign content
      const contentResponse = await this.fetch(
        `https://${serverPrefix}.api.mailchimp.com/3.0/campaigns/${campaignData.id}/content`,
        {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            html: emailBody,
          }),
        }
      );

      if (!contentResponse.ok) {
        return {
          success: false,
          platform: this.platform,
          error: 'Failed to set campaign content',
        };
      }

      this.log('Campaign content set successfully');

      return {
        success: true,
        platform: this.platform,
        url: `https://mailchimp.com/campaigns/${campaignData.id}`,
        metadata: {
          provider: 'mailchimp',
          campaignId: campaignData.id,
          draft: true,
        },
      };
    } catch (error: any) {
      this.logError('Mailchimp publish error:', error);
      return {
        success: false,
        platform: this.platform,
        error: error.message || 'Mailchimp API error',
      };
    }
  }

  /**
   * Generate email subject line
   */
  private generateEmailSubject(title: string): string {
    // Truncate to reasonable length for email subject
    const maxLength = 60;
    if (title.length > maxLength) {
      return title.substring(0, maxLength - 3) + '...';
    }
    return title;
  }

  /**
   * Format content for email (HTML)
   */
  private formatEmailBody(content: PlatformContent): string {
    const styles = `
      <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; }
        img { max-width: 100%; height: auto; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; }
        pre { background: #f4f4f4; padding: 12px; border-radius: 6px; overflow-x: auto; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .divider { border-top: 1px solid #ddd; margin: 24px 0; }
        .footer { color: #666; font-size: 12px; margin-top: 32px; }
      </style>
    `;

    const header = `
      <h1>${this.escapeHtml(content.title)}</h1>
      ${content.excerpt ? `<p><strong>${this.escapeHtml(content.excerpt)}</strong></p>` : ''}
    `;

    const footer = `
      <div class="divider"></div>
      <div class="footer">
        <p>Read the full article: <a href="${content.canonicalUrl}">${this.escapeHtml(content.title)}</a></p>
        <p>Tags: ${content.tags.map(tag => `<code>${this.escapeHtml(tag)}</code>`).join(', ')}</p>
        <p>Published by ACIDBATH</p>
      </div>
    `;

    return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  ${styles}
</head>
<body>
  ${header}
  ${content.content}
  ${footer}
</body>
</html>`;
  }

  /**
   * Escape HTML special characters
   */
  private escapeHtml(text: string): string {
    const htmlEscapeMap: Record<string, string> = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
    };
    return text.replace(/[&<>"']/g, char => htmlEscapeMap[char]);
  }

  /**
   * Save publish log after successful publish
   */
  async publish(content: PlatformContent): Promise<PublishResult> {
    const result = await super.publish(content);

    // Save publish log
    if (result.success) {
      const slug = content.metadata?.slug || 'unknown';
      await this.savePublishLog(slug, result);
    }

    return result;
  }
}

export default NewsletterPublisher;
