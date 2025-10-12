"use client"

import { useAuth } from "@/lib/auth-context"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Copy, Check, Key } from "lucide-react"
import { useState } from "react"

interface TokenInfoDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function TokenInfoDialog({ open, onOpenChange }: TokenInfoDialogProps) {
  const { accessToken, refreshToken } = useAuth()
  const [copiedAccess, setCopiedAccess] = useState(false)
  const [copiedRefresh, setCopiedRefresh] = useState(false)

  const copyToClipboard = async (text: string, type: "access" | "refresh") => {
    try {
      await navigator.clipboard.writeText(text)
      if (type === "access") {
        setCopiedAccess(true)
        setTimeout(() => setCopiedAccess(false), 2000)
      } else {
        setCopiedRefresh(true)
        setTimeout(() => setCopiedRefresh(false), 2000)
      }
    } catch (err) {
      console.error("خطا در کپی کردن:", err)
    }
  }

  const truncateToken = (token: string) => {
    if (token.length <= 40) return token
    return `${token.substring(0, 20)}...${token.substring(token.length - 20)}`
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
              <Key className="h-6 w-6 text-primary" />
            </div>
            <div>
              <DialogTitle>اطلاعات توکن‌های احراز هویت</DialogTitle>
              <DialogDescription>مشاهده و مدیریت توکن‌های دسترسی</DialogDescription>
            </div>
          </div>
        </DialogHeader>

        <div className="space-y-4">
          {/* Access Token */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium">توکن دسترسی (Access Token)</label>
              <Button size="sm" variant="ghost" onClick={() => accessToken && copyToClipboard(accessToken, "access")}>
                {copiedAccess ? (
                  <>
                    <Check className="ml-2 h-3 w-3" />
                    کپی شد
                  </>
                ) : (
                  <>
                    <Copy className="ml-2 h-3 w-3" />
                    کپی
                  </>
                )}
              </Button>
            </div>
            <div className="p-3 rounded-lg bg-muted border border-border font-mono text-xs break-all">
              {accessToken ? truncateToken(accessToken) : "توکنی یافت نشد"}
            </div>
            <p className="text-xs text-muted-foreground">
              این توکن برای احراز هویت درخواست‌های API استفاده می‌شود و معمولا در 5-15 دقیقه منقضی می‌شود.
            </p>
          </div>

          {/* Refresh Token */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium">توکن تازه‌سازی (Refresh Token)</label>
              <Button
                size="sm"
                variant="ghost"
                onClick={() => refreshToken && copyToClipboard(refreshToken, "refresh")}
              >
                {copiedRefresh ? (
                  <>
                    <Check className="ml-2 h-3 w-3" />
                    کپی شد
                  </>
                ) : (
                  <>
                    <Copy className="ml-2 h-3 w-3" />
                    کپی
                  </>
                )}
              </Button>
            </div>
            <div className="p-3 rounded-lg bg-muted border border-border font-mono text-xs break-all">
              {refreshToken ? truncateToken(refreshToken) : "توکنی یافت نشد"}
            </div>
            <p className="text-xs text-muted-foreground">
              این توکن برای دریافت توکن دسترسی جدید استفاده می‌شود و معمولا عمر طولانی‌تری دارد.
            </p>
          </div>

          {/* Security Warning */}
          <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/20">
            <p className="text-sm text-destructive font-medium mb-1">هشدار امنیتی</p>
            <p className="text-xs text-destructive/80">
              این توکن‌ها اطلاعات حساس هستند. آن‌ها را با کسی به اشتراک نگذارید و در مکان‌های امن نگهداری کنید.
            </p>
          </div>
        </div>

        <div className="flex justify-end">
          <Button onClick={() => onOpenChange(false)}>بستن</Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
