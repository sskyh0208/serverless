import { Loader2 } from "lucide-react"

type Props = {
  height?: number;
  width?: number;
}

export const LoadingIcon = ({
  height,
  width,
}: Props) => {
  return (
    <Loader2
      height={height ?? 48}
      width={width ?? 48}
      className="animate-spin text-cyan-700"
    />
  )
}