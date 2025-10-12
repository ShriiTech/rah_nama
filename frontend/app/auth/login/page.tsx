"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { authAPI } from "@/lib/api"
import { useAuth } from "@/lib/auth-context"
import { Loader2, Lock, Mail } from "lucide-react"

export default function LoginPage() {
  const [step, setStep] = useState<"request" | "verify">("request")
  const [phoneOrEmail, setPhoneOrEmail] = useState("")
  const [otp, setOtp] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const router = useRouter()
  const { login } = useAuth()

  const handleRequestOTP = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setLoading(true)

    try {
      await authAPI.requestOTP(phoneOrEmail)
      setStep("verify")
    } catch (err: any) {
      setError(err.message || "خطا در ارسال کد تایید")
    } finally {
      setLoading(false)
    }
  }

  const handleVerifyOTP = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setLoading(true)

    try {
      const response = await authAPI.verifyOTP(phoneOrEmail, otp)
      login(response.access, response.refresh)
      router.push("/dashboard")
    } catch (err: any) {
      setError(err.message || "کد تایید نامعتبر است")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md border-border">
        <CardHeader className="space-y-2">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 rounded-xl bg-primary/10 flex items-center justify-center">
              <Lock className="w-8 h-8 text-primary" />
            </div>
          </div>
          <CardTitle className="text-2xl text-center">ورود به سیستم</CardTitle>
          <CardDescription className="text-center">
            {step === "request"
              ? "برای ورود، ایمیل یا شماره موبایل خود را وارد کنید"
              : "کد تایید ارسال شده را وارد کنید"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {step === "request" ? (
            <form onSubmit={handleRequestOTP} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="phoneOrEmail">ایمیل یا شماره موبایل</Label>
                <div className="relative">
                  <Mail className="absolute right-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="phoneOrEmail"
                    type="text"
                    placeholder="example@email.com یا 09123456789"
                    value={phoneOrEmail}
                    onChange={(e) => setPhoneOrEmail(e.target.value)}
                    className="pr-10"
                    required
                    disabled={loading}
                  />
                </div>
              </div>

              {error && (
                <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20">
                  <p className="text-sm text-destructive">{error}</p>
                </div>
              )}

              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                    در حال ارسال...
                  </>
                ) : (
                  "ارسال کد تایید"
                )}
              </Button>
            </form>
          ) : (
            <form onSubmit={handleVerifyOTP} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="otp">کد تایید</Label>
                <Input
                  id="otp"
                  type="text"
                  placeholder="کد 6 رقمی"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  maxLength={6}
                  className="text-center text-2xl tracking-widest"
                  required
                  disabled={loading}
                  autoFocus
                />
              </div>

              {error && (
                <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20">
                  <p className="text-sm text-destructive">{error}</p>
                </div>
              )}

              <div className="space-y-2">
                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? (
                    <>
                      <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                      در حال تایید...
                    </>
                  ) : (
                    "تایید و ورود"
                  )}
                </Button>
                <Button
                  type="button"
                  variant="ghost"
                  className="w-full"
                  onClick={() => {
                    setStep("request")
                    setOtp("")
                    setError("")
                  }}
                  disabled={loading}
                >
                  تغییر شماره یا ایمیل
                </Button>
              </div>
            </form>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
