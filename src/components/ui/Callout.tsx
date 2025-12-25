import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

type CalloutType =
  | "quote"
  | "info"
  | "warning"
  | "danger"
  | "success"
  | "insight"
  | "data";

interface CalloutProps {
  type: CalloutType;
  title?: string;
  author?: string;
  children: ReactNode;
}

const variants: Record<
  CalloutType,
  {
    icon: string;
    borderColor: string;
    bgColor: string;
    textColor: string;
    defaultTitle: string;
  }
> = {
  quote: {
    icon: '"',
    borderColor: "border-muted-foreground",
    bgColor: "bg-transparent",
    textColor: "text-muted-foreground",
    defaultTitle: "Quote",
  },
  info: {
    icon: "i",
    borderColor: "border-blue-500",
    bgColor: "bg-blue-500/10",
    textColor: "text-blue-500",
    defaultTitle: "Info",
  },
  warning: {
    icon: "!",
    borderColor: "border-orange-500",
    bgColor: "bg-orange-500/10",
    textColor: "text-orange-500",
    defaultTitle: "Warning",
  },
  danger: {
    icon: "x",
    borderColor: "border-red-500",
    bgColor: "bg-red-500/10",
    textColor: "text-red-500",
    defaultTitle: "Danger",
  },
  success: {
    icon: "v",
    borderColor: "border-green-500",
    bgColor: "bg-green-500/10",
    textColor: "text-green-500",
    defaultTitle: "Success",
  },
  insight: {
    icon: "*",
    borderColor: "border-primary",
    bgColor: "bg-primary/10",
    textColor: "text-primary",
    defaultTitle: "Key Insight",
  },
  data: {
    icon: "#",
    borderColor: "border-purple-500",
    bgColor: "bg-purple-500/10",
    textColor: "text-purple-500",
    defaultTitle: "Data",
  },
};

export function Callout({ type, title, author, children }: CalloutProps) {
  const variant = variants[type];
  const displayTitle = title || variant.defaultTitle;

  if (type === "quote") {
    return (
      <blockquote
        className={cn(
          "relative my-6 pl-8 border-l-2",
          variant.borderColor,
          variant.bgColor
        )}
      >
        <span className="absolute left-2 top-0 text-4xl font-bold opacity-30 text-muted-foreground leading-none">
          "
        </span>
        <div className="italic text-lg text-muted-foreground">{children}</div>
        {author && (
          <footer className="mt-4 font-semibold text-right text-muted-foreground not-italic">
            — {author}
          </footer>
        )}
      </blockquote>
    );
  }

  return (
    <Alert
      className={cn(
        "my-6 border-l-2 rounded-sm",
        variant.borderColor,
        variant.bgColor,
        type === "insight" && "border-l-4 bg-gradient-to-br from-primary/10 to-transparent"
      )}
    >
      <div className={cn("flex items-center gap-2 mb-3", variant.textColor)}>
        <span className="text-lg font-bold leading-none">{variant.icon}</span>
        <AlertTitle className="uppercase text-sm font-bold tracking-wider m-0">
          {displayTitle}
        </AlertTitle>
      </div>
      <AlertDescription className="text-foreground leading-relaxed [&>p:first-child]:mt-0 [&>p:last-child]:mb-0">
        {children}
      </AlertDescription>
    </Alert>
  );
}
