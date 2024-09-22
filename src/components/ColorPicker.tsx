import { Button } from "~/components/ui/button";
import { Input } from "~/components/ui/input";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "~/components/ui/popover";
import { cn } from "~/lib/utils";
import { Paintbrush } from "lucide-react";
import { GeistSans } from "geist/font/sans";

export default function ColorPicker({
  colors,
  color,
  setColor,
  className,
}: {
  colors: string[];
  color: string;
  setColor: (background: string) => void;
  className?: string;
}) {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant={"outline"}
          className={cn(
            "w-[220px] justify-start text-left",
            !color && "text-muted-foreground",
            className,
          )}
        >
          <div className="flex w-full items-center gap-2">
            {color ? (
              <div
                className="h-4 w-4 rounded !bg-cover !bg-center transition-all"
                style={{ background: color }}
              ></div>
            ) : (
              <Paintbrush className="h-4 w-4" />
            )}
            <div className="flex-1 truncate">{color || "Pick a color"}</div>
          </div>
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-64">
        <div className="mb-4 mt-0 flex w-full flex-wrap gap-1">
          {colors.map((s) => (
            <div
              key={s}
              style={{ background: s }}
              className="h-6 w-6 cursor-pointer rounded-md hover:scale-105"
              onClick={() => setColor(s)}
            />
          ))}
        </div>

        <Input
          id="custom"
          value={color}
          className={cn("col-span-2 mt-4 h-8", GeistSans.className)}
          onChange={(e) => setColor(e.currentTarget.value)}
        />
      </PopoverContent>
    </Popover>
  );
}
