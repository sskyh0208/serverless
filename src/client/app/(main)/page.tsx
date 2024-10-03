"use client";

import { useEffect, useState } from 'react';
import { LoadingIcon } from '@/components/LoadingIcon';

export default function CoursesPage() {
  const [isLoading, setIsLoading] = useState(true);
  
  return (
    <div className="h-full max-w-[912px] px-3 mx-auto">
      <h1 className="text-2xl font-bold text-neutral-700">
        メインページ
      </h1>
    </div>
  )
}
