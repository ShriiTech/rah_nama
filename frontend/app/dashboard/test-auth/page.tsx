"use client"

import { useState } from "react"
import { useAuth } from "@/lib/auth-context"
import { authAPI } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { DashboardHeader } from "@/components/dashboard-header"
import { Loader2, CheckCircle2, XCircle, TestTube } from "lucide-react"

export default function TestAuthPage() {
  const { accessToken } = useAuth()
  const [testing, setTesting] = useState(false)
  const [result, setResult] = useState<{ success: boolean; message: string } | null>(null)

  const handleTestAuth = async () => {
    if (!accessToken) return

    setTesting(true)
    setResult(null)

    try {
      const response = await authAPI.testAuth(accessToken)
      setResult({
        success: true,
        message: "احراز هویت موفقیت‌آمیز بود! توکن شما معتبر است.",
      })
    } catch (err: any) {
      setResult({
        success: false,
        message: err.message || "احراز هویت ناموفق بود. توکن شما نامعتبر است.",
      })
    } finally {
      setTesting(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />

      <main className="container mx-auto p-6">
        <Card className="max-w-2xl mx-auto border-border">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                <TestTube className="h-6 w-6 text-primary" />
              </div>
              <div>
                <CardTitle className="text-2xl">تست احراز هویت</CardTitle>
                <CardDescription>بررسی اعتبار توکن دسترسی شما</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="p-4 rounded-lg bg-muted border border-border">
              <p className="text-sm text-muted-foreground">
                این صفحه برای تست endpoint احراز هویت API طراحی شده است. با کلیک بر روی دکمه زیر، یک درخواست به سرور
                ارسال می‌شود تا اعتبار توکن دسترسی شما بررسی شود.
              </p>
            </div>

            <Button onClick={handleTestAuth} disabled={testing} className="w-full" size="lg">
              {testing ? (
                <>
                  <Loader2 className="ml-2 h-5 w-5 animate-spin" />
                  در حال تست...
                </>
              ) : (
                <>
                  <TestTube className="ml-2 h-5 w-5" />
                  تست احراز هویت
                </>
              )}
            </Button>

            {result && (
              <div
                className={`p-4 rounded-lg border ${
                  result.success ? "bg-green-500/10 border-green-500/20" : "bg-destructive/10 border-destructive/20"
                }`}
              >
                <div className="flex items-start gap-3">
                  {result.success ? (
                    <CheckCircle2 className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                  ) : (
                    <XCircle className="h-5 w-5 text-destructive mt-0.5 flex-shrink-0" />
                  )}
                  <div>
                    <p className={`font-medium ${result.success ? "text-green-500" : "text-destructive"}`}>
                      {result.success ? "موفقیت‌آمیز" : "ناموفق"}
                    </p>
                    <p className="text-sm mt-1">{result.message}</p>
                  </div>
                </div>
              </div>
            )}

            <div className="space-y-3">
              <h3 className="font-medium">اطلاعات تکنیکی:</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between p-2 rounded bg-muted">
                  <span className="text-muted-foreground">Endpoint:</span>
                  <span className="font-mono">/test-auth</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-muted">
                  <span className="text-muted-foreground">Method:</span>
                  <span className="font-mono">GET</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-muted">
                  <span className="text-muted-foreground">Authorization:</span>
                  <span className="font-mono">Bearer Token</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
