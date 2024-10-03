"use client";

import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { ReactNode } from "react";
import { cn } from "@/lib/utils";

type Props = {
  label: string;
  icon: ReactNode;
  href?: string;
  onClick?: () => void;
  disabled?: boolean;
}

export const SidebarItem = ({
  label,
  icon,
  href,
  onClick,
  disabled,
}: Props) => {
  const pathname = usePathname();
  const isActive = pathname === href;

  const content = (
    <>
      <div className="mr-2">
        { icon }
      </div>
      <div className="flex flex-col text-left text-xs">
        <p>{ label }</p>
      </div>
    </>
  );

  return (
    <Button
      className={cn(
        "justify-start h-[52px] w-full transition-all duration-500 ease-out hover:bg-white/50 hover:text-black",
        isActive && "border-2"
      )}
      onClick={onClick}
      asChild={!onClick}
      disabled={disabled}
    >
      {onClick ? content : <Link href={href!}>{content}</Link>}
    </Button>
  )
}