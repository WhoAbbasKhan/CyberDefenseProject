import './globals.css'
import type { Metadata } from 'next'
import { Toaster } from 'sonner'

export const metadata: Metadata = {
    title: 'Cyber Defense Command Center',
    description: 'Advanced Cyber Defense Platform',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body>
                {children}
                <Toaster richColors position="top-right" />
            </body>
        </html>
    )
}
