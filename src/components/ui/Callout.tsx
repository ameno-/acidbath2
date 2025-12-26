import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { cn } from "@/lib/utils";
import type { ReactNode } from "react";
import { Info, Lightbulb, TriangleAlert, OctagonAlert, Quote } from "lucide-react";

type CalloutType =
  | "note"
  | "tip"
  | "info"
  | "warning"
  | "danger"
  | "quote";

interface CalloutProps {
  type: CalloutType;
  title?: string;
  author?: string;
  children: ReactNode;
}

const variants: Record<
  CalloutType,
  {
    Icon: any;
    borderColor: string;
    bgColor: string;
    textColor: string;
    defaultTitle: string;
  }
> = {
  note: {
    Icon: Info,
    borderColor: "border-blue-900",
    bgColor: "bg-blue-950/50",
    textColor: "text-blue-400",
    defaultTitle: "Note",
  },
  tip: {
    Icon: Lightbulb,
    borderColor: "border-purple-900",
    bgColor: "bg-purple-950/50",
    textColor: "text-purple-400",
    defaultTitle: "Tip",
  },
  info: {
    Icon: Info,
    borderColor: "border-blue-900",
    bgColor: "bg-blue-950/50",
    textColor: "text-blue-400",
    defaultTitle: "Info",
  },
  warning: {
    Icon: TriangleAlert,
    borderColor: "border-amber-900",
    bgColor: "bg-amber-950/50",
    textColor: "text-amber-400",
    defaultTitle: "Warning",
  },
  danger: {
    Icon: OctagonAlert,
    borderColor: "border-red-900",
    bgColor: "bg-red-950/50",
    textColor: "text-red-400",
    defaultTitle: "Danger",
  },
  quote: {
    Icon: Quote,
    borderColor: "border-slate-300",
    bgColor: "bg-slate-900/50",
    textColor: "text-slate-300",
    defaultTitle: "Quote",
  },
};

export function Callout({ type, title, author, children }: CalloutProps) {
  const variant = variants[type];
  const displayTitle = title || variant.defaultTitle;
  const Icon = variant.Icon;

  if (type === "quote") {
    return (
      <blockquote
        className={cn(
          "relative my-6 pl-8 border-l-4 rounded-sm p-4",
          variant.borderColor,
          variant.bgColor
        )}
      >
        <div className="flex items-start gap-3">
          <Icon className={cn("w-5 h-5 flex-shrink-0 mt-1", variant.textColor)} />
          <div className="flex-1">
            <div className="italic text-lg text-muted-foreground">{children}</div>
            {author && (
              <footer className="mt-4 font-semibold text-right text-muted-foreground not-italic">
                — {author}
              </footer>
            )}
          </div>
        </div>
      </blockquote>
    );
  }

  return (
    <Alert
      className={cn(
        "my-6 border-l-2 rounded-sm",
        variant.borderColor,
        variant.bgColor
      )}
    >
      <div className={cn("flex items-center gap-2 mb-3", variant.textColor)}>
        <Icon className="w-5 h-5" />
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
