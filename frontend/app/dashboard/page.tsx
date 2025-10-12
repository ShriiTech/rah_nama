"use client"

import { useState, useEffect } from "react"
import { useAuth } from "@/lib/auth-context"
import { userAPI } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Loader2, Plus, Users } from "lucide-react"
import { DashboardHeader } from "@/components/dashboard-header"
import { CreateUserDialog } from "@/components/create-user-dialog"
import { EditUserDialog } from "@/components/edit-user-dialog"
import { DeleteUserDialog } from "@/components/delete-user-dialog"

interface User {
  id: number
  username?: string
  email?: string
  phone?: string
  first_name?: string
  last_name?: string
  is_active?: boolean
}

export default function DashboardPage() {
  const { accessToken } = useAuth()
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [createDialogOpen, setCreateDialogOpen] = useState(false)
  const [editUser, setEditUser] = useState<User | null>(null)
  const [deleteUser, setDeleteUser] = useState<User | null>(null)

  const fetchUsers = async () => {
    if (!accessToken) return

    setLoading(true)
    setError("")

    try {
      const data = await userAPI.getUsers(accessToken)
      setUsers(data)
    } catch (err: any) {
      setError(err.message || "خطا در دریافت لیست کاربران")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchUsers()
  }, [accessToken])

  const handleUserCreated = () => {
    setCreateDialogOpen(false)
    fetchUsers()
  }

  const handleUserUpdated = () => {
    setEditUser(null)
    fetchUsers()
  }

  const handleUserDeleted = () => {
    setDeleteUser(null)
    fetchUsers()
  }

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />

      <main className="container mx-auto p-6 space-y-6">
        <Card className="border-border">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <CardTitle className="text-2xl flex items-center gap-2">
                  <Users className="h-6 w-6" />
                  مدیریت کاربران
                </CardTitle>
                <CardDescription>مشاهده و مدیریت کاربران سیستم</CardDescription>
              </div>
              <Button onClick={() => setCreateDialogOpen(true)}>
                <Plus className="ml-2 h-4 w-4" />
                افزودن کاربر جدید
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <div className="flex flex-col items-center gap-4">
                  <Loader2 className="h-8 w-8 animate-spin text-primary" />
                  <p className="text-muted-foreground">در حال بارگذاری...</p>
                </div>
              </div>
            ) : error ? (
              <div className="p-6 rounded-lg bg-destructive/10 border border-destructive/20">
                <p className="text-destructive text-center">{error}</p>
                <div className="flex justify-center mt-4">
                  <Button onClick={fetchUsers} variant="outline">
                    تلاش مجدد
                  </Button>
                </div>
              </div>
            ) : users.length === 0 ? (
              <div className="text-center py-12">
                <Users className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                <p className="text-muted-foreground">هیچ کاربری یافت نشد</p>
                <Button onClick={() => setCreateDialogOpen(true)} className="mt-4" variant="outline">
                  <Plus className="ml-2 h-4 w-4" />
                  افزودن اولین کاربر
                </Button>
              </div>
            ) : (
              <div className="rounded-lg border border-border overflow-hidden">
                <Table>
                  <TableHeader>
                    <TableRow className="bg-muted/50">
                      <TableHead className="text-right">شناسه</TableHead>
                      <TableHead className="text-right">نام کاربری</TableHead>
                      <TableHead className="text-right">ایمیل</TableHead>
                      <TableHead className="text-right">نام</TableHead>
                      <TableHead className="text-right">نام خانوادگی</TableHead>
                      <TableHead className="text-right">وضعیت</TableHead>
                      <TableHead className="text-right">عملیات</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {users.map((user) => (
                      <TableRow key={user.id}>
                        <TableCell className="font-mono">{user.id}</TableCell>
                        <TableCell>{user.username || "-"}</TableCell>
                        <TableCell className="font-mono text-sm">{user.email || "-"}</TableCell>
                        <TableCell>{user.first_name || "-"}</TableCell>
                        <TableCell>{user.last_name || "-"}</TableCell>
                        <TableCell>
                          <span
                            className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                              user.is_active
                                ? "bg-green-500/10 text-green-500 border border-green-500/20"
                                : "bg-red-500/10 text-red-500 border border-red-500/20"
                            }`}
                          >
                            {user.is_active ? "فعال" : "غیرفعال"}
                          </span>
                        </TableCell>
                        <TableCell>
                          <div className="flex gap-2">
                            <Button size="sm" variant="outline" onClick={() => setEditUser(user)}>
                              ویرایش
                            </Button>
                            <Button size="sm" variant="destructive" onClick={() => setDeleteUser(user)}>
                              حذف
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>
      </main>

      <CreateUserDialog open={createDialogOpen} onOpenChange={setCreateDialogOpen} onSuccess={handleUserCreated} />

      {editUser && (
        <EditUserDialog
          user={editUser}
          open={!!editUser}
          onOpenChange={(open) => !open && setEditUser(null)}
          onSuccess={handleUserUpdated}
        />
      )}

      {deleteUser && (
        <DeleteUserDialog
          user={deleteUser}
          open={!!deleteUser}
          onOpenChange={(open) => !open && setDeleteUser(null)}
          onSuccess={handleUserDeleted}
        />
      )}
    </div>
  )
}
