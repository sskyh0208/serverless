import { useState } from 'react';
import { cn } from "@/lib/utils"
import { SidebarItem } from "@/components/SidebarItem"
import { BookOpen, ChartColumn, LogOut, Upload } from "lucide-react"
import { useRouter } from 'next/navigation';

type Props = {
  className?: string
}

export const Sidebar = ({
  className
}: Props) => {
  const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false);
  const router = useRouter();

  const menus = [
    {
      id: 1,
      label: "files",
      href: "/files",
      icon: <Upload size={24} />,
    },
  ]
  
  return (
    <div className={cn(
      "flex h-full lg:w-[256px] lg:fixed left-0 top-0 px-4 lg:border-r-2 flex-col",
      className
    )}>
      <div className="flex flex-col justify-between h-full py-4 gap-y-2">
        {menus.map((menu) => (
          <SidebarItem
            key={menu.id}
            label={menu.label}
            href={menu.href}
            icon={menu.icon}
          />
        )
        )}
      </div>
    </div>
  )
}