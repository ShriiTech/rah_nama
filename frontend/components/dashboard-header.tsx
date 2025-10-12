"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/lib/auth-context"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { LogOut, Shield, User, RefreshCw, Key } from "lucide-react"
import { TokenInfoDialog } from "./token-info-dialog"

export function DashboardHeader() {
  const { logout, refreshAccessToken } = useAuth()
  const router = useRouter()
  const [tokenDialogOpen, setTokenDialogOpen] = useState(false)
  const [refreshing, setRefreshing] = useState(false)

  const handleLogout = async () => {
    await logout()
    router.push("/auth/login")
  }

  const handleRefreshToken = async () => {
    setRefreshing(true)
    const success = await refreshAccessToken()
    setRefreshing(false)

    if (success) {
      // Show success feedback (you could add a toast notification here)
      console.log("توکن با موفقیت تازه‌سازی شد")
    }
  }

  return (
    <>
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <Shield className="h-6 w-6 text-primary" />
              </div>
              <div>
                <h1 className="text-xl font-bold">پنل مدیریت</h1>
                <p className="text-sm text-muted-foreground">سیستم مدیریت کاربران</p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="icon">
                    <User className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-56">
                  <DropdownMenuLabel>حساب کاربری</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={() => setTokenDialogOpen(true)}>
                    <Key className="ml-2 h-4 w-4" />
                    اطلاعات توکن
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={handleRefreshToken} disabled={refreshing}>
                    <RefreshCw className={`ml-2 h-4 w-4 ${refreshing ? "animate-spin" : ""}`} />
                    تازه‌سازی توکن
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={handleLogout} className="text-destructive focus:text-destructive">
                    <LogOut className="ml-2 h-4 w-4" />
                    خروج از سیستم
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </div>
      </header>

      <TokenInfoDialog open={tokenDialogOpen} onOpenChange={setTokenDialogOpen} />
    </>
  )
}
