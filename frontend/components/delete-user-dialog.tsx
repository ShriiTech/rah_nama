"use client"

import { useState } from "react"
import { useAuth } from "@/lib/auth-context"
import { userAPI } from "@/lib/api"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Loader2, AlertTriangle } from "lucide-react"

interface User {
  id: number
  username?: string
  email?: string
}

interface DeleteUserDialogProps {
  user: User
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess: () => void
}

export function DeleteUserDialog({ user, open, onOpenChange, onSuccess }: DeleteUserDialogProps) {
  const { accessToken } = useAuth()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleDelete = async () => {
    if (!accessToken) return

    setError("")
    setLoading(true)

    try {
      await userAPI.deleteUser(accessToken, user.id)
      onSuccess()
    } catch (err: any) {
      setError(err.message || "خطا در حذف کاربر")
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-destructive/10 flex items-center justify-center">
              <AlertTriangle className="h-6 w-6 text-destructive" />
            </div>
            <div>
              <DialogTitle>حذف کاربر</DialogTitle>
              <DialogDescription>آیا از حذف این کاربر اطمینان دارید؟</DialogDescription>
            </div>
          </div>
        </DialogHeader>
        <div className="space-y-4">
          <div className="p-4 rounded-lg bg-muted border border-border">
            <p className="text-sm">
              <span className="font-medium">نام کاربری:</span> {user.username || "نامشخص"}
            </p>
            {user.email && (
              <p className="text-sm mt-1">
                <span className="font-medium">ایمیل:</span> {user.email}
              </p>
            )}
          </div>

          <p className="text-sm text-muted-foreground">
            این عملیات قابل بازگشت نیست. تمام اطلاعات مربوط به این کاربر حذف خواهد شد.
          </p>

          {error && (
            <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20">
              <p className="text-sm text-destructive">{error}</p>
            </div>
          )}

          <div className="flex gap-2 justify-end">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)} disabled={loading}>
              انصراف
            </Button>
            <Button variant="destructive" onClick={handleDelete} disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                  در حال حذف...
                </>
              ) : (
                "حذف کاربر"
              )}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
