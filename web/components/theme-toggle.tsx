"use client";

import { Monitor, Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

const CHOICES = [
  { value: "light", label: "Light", Icon: Sun },
  { value: "dark", label: "Dark", Icon: Moon },
  { value: "system", label: "Match this computer", Icon: Monitor },
] as const;

/**
 * Three states, not two. A toggle that only offers light and dark quietly overrides the
 * preference a person already set on their machine, and then never gives it back.
 *
 * Rendered as a radio group rather than as buttons, because that is what it is: one choice out
 * of three, arrow keys move between them, and a screen reader says "Dark, radio button, 2 of 3"
 * instead of "Dark, button" three times with no indication of which is on.
 */
export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [ready, setReady] = useState(false);

  // The server cannot know the choice, so the first client render must match the server's.
  useEffect(() => setReady(true), []);

  return (
    <fieldset
      className="flex items-center gap-px rounded-[var(--r-pill)] border border-hairline bg-surface-2 p-px"
      aria-label="Colour theme"
    >
      {CHOICES.map(({ value, label, Icon }) => {
        const on = ready && theme === value;
        return (
          <label
            key={value}
            title={label}
            className={[
              "grid h-7 w-8 cursor-pointer place-items-center rounded-[var(--r-pill)]",
              "transition-colors duration-[var(--dur-press)]",
              "focus-within:outline-2 focus-within:outline-offset-2 focus-within:outline-focus",
              on ? "bg-surface text-accent shadow-lift-1" : "text-ink-3 hover:text-ink-2",
            ].join(" ")}
          >
            <input
              type="radio"
              name="parrot-theme"
              value={value}
              checked={on}
              onChange={() => setTheme(value)}
              className="sr-only"
            />
            <Icon aria-hidden size={14} strokeWidth={2} />
            <span className="sr-only">{label}</span>
          </label>
        );
      })}
    </fieldset>
  );
}
