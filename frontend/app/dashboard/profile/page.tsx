"use client";

import { TopBar } from "@/components/layout/TopBar";
import { Sidebar } from "@/components/layout/Sidebar";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { DeviceHistoryList } from "@/components/security/DeviceHistoryList";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { User, Lock, Shield } from "lucide-react";

export default function ProfilePage() {
    return (
        <div className="flex h-screen bg-background font-sans dark">
            <Sidebar className="w-64 border-r hidden md:block" />
            <div className="flex-1 flex flex-col overflow-hidden">
                <TopBar />
                <main className="flex-1 overflow-y-auto p-6 space-y-6">
                    <h2 className="text-2xl font-bold tracking-tight">User Settings</h2>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {/* Profile Info */}
                        <div className="col-span-1 space-y-6">
                            <Card>
                                <CardHeader>
                                    <CardTitle className="text-lg">Profile Information</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium">Full Name</label>
                                        <div className="flex items-center gap-2">
                                            <User className="w-4 h-4 text-muted-foreground" />
                                            <Input defaultValue="Admin User" readOnly />
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium">Email</label>
                                        <Input defaultValue="admin@velvet.net" readOnly />
                                    </div>
                                    <Button className="w-full">Update Profile</Button>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Security & Devices */}
                        <div className="col-span-2 space-y-6">
                            <Card>
                                <CardHeader>
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <CardTitle className="text-lg flex items-center gap-2">
                                                <Lock className="w-5 h-5 text-blue-500" />
                                                Security & Sessions
                                            </CardTitle>
                                            <CardDescription>Manage your active devices and sessions.</CardDescription>
                                        </div>
                                        <Button variant="outline" size="sm">Sign Out All Devices</Button>
                                    </div>
                                </CardHeader>
                                <CardContent>
                                    <DeviceHistoryList />
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                </main>
            </div>
        </div>
    );
}
