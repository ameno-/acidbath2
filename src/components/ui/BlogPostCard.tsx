import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface BlogPostCardProps {
  title: string;
  description: string;
  pubDate: Date;
  slug: string;
  tags?: string[];
}

export function BlogPostCard({
  title,
  description,
  pubDate,
  slug,
  tags = [],
}: BlogPostCardProps) {
  const formattedDate = pubDate.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  return (
    <Card className="border-border/50 bg-transparent hover:border-primary/50 hover:bg-card/30 transition-all duration-200 group">
      <CardHeader className="pb-3">
        <time
          dateTime={pubDate.toISOString()}
          className="text-sm text-muted-foreground font-mono"
        >
          {formattedDate}
        </time>
        <CardTitle className="text-lg font-bold normal-case tracking-normal">
          <a
            href={`/blog/${slug}`}
            className="hover:text-primary transition-colors no-underline group-hover:underline decoration-2 underline-offset-4"
          >
            {title}
          </a>
        </CardTitle>
        <CardDescription className="text-muted-foreground leading-relaxed">
          {description}
        </CardDescription>
      </CardHeader>
      {tags.length > 0 && (
        <CardContent className="pt-0">
          <div className="flex flex-wrap gap-2 [&>*]:mt-0">
            {tags.map((tag) => (
              <a key={tag} href={`/tags/${tag}`} className="no-underline mt-0">
                <Badge
                  variant="outline"
                  className="text-xs hover:bg-primary hover:text-primary-foreground hover:border-primary transition-colors cursor-pointer"
                >
                  {tag}
                </Badge>
              </a>
            ))}
          </div>
        </CardContent>
      )}
    </Card>
  );
}
