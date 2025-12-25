"use client";

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { cn } from "@/lib/utils";
import { useState, type ReactNode } from "react";

type CollapseVariant = "default" | "compact" | "prominent";

interface CollapseProps {
  title: string;
  preview?: string;
  variant?: CollapseVariant;
  defaultOpen?: boolean;
  children: ReactNode;
}

export function Collapse({
  title,
  preview,
  variant = "default",
  defaultOpen = false,
  children,
}: CollapseProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <Collapsible
      open={isOpen}
      onOpenChange={setIsOpen}
      className={cn(
        "my-6 border-2 border-foreground rounded-sm bg-background transition-colors",
        "hover:bg-secondary/30",
        variant === "compact" && "my-4",
        variant === "prominent" && "border-primary border-l-4 hover:bg-primary/5"
      )}
    >
      <CollapsibleTrigger
        className={cn(
          "flex w-full items-center gap-2 p-4 cursor-pointer select-none font-semibold",
          "transition-colors hover:text-primary group",
          variant === "compact" && "p-3"
        )}
      >
        <span
          className={cn(
            "text-sm text-muted-foreground transition-transform duration-150 min-w-[1em]",
            "group-hover:text-primary",
            isOpen && "rotate-90"
          )}
        >
          ▸
        </span>
        <span
          className={cn(
            "flex-1 text-left font-bold uppercase tracking-wider text-sm",
            variant === "prominent" && "text-primary"
          )}
        >
          {title}
        </span>
        {preview && !isOpen && (
          <span className="text-sm text-muted-foreground font-normal italic ml-2">
            {preview}
          </span>
        )}
        <span className="ml-auto text-xs text-muted-foreground/70 uppercase tracking-widest font-medium">
          {isOpen ? "Collapse" : "Expand"}
        </span>
      </CollapsibleTrigger>
      <CollapsibleContent>
        <div
          className={cn(
            "border-t border-muted-foreground/30 mt-2 pt-4 px-4 pb-4",
            "[&>*:first-child]:mt-0 [&>*:last-child]:mb-0",
            "[&>*+*]:mt-4",
            variant === "compact" && "px-3 pb-3 pt-3"
          )}
        >
          {children}
        </div>
      </CollapsibleContent>
    </Collapsible>
  );
}
