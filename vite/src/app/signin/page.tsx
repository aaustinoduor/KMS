"use client"
import { Button } from "antd"
import { useState } from "react"
import { HiEyeSlash as HidePasswordIcon, HiEye as ShowPasswordIcon } from "react-icons/hi2"
import { FcGoogle } from "react-icons/fc" // Google Icon

export default function SignIn() {
    const [showPassword, setShowPassword] = useState<boolean>(false)

    return (
        <main className="flex justify-center items-center h-dvh text-gray-100">
            <form method="POST" className="flex flex-col gap-y-5 bg-gray-800 shadow-lg p-8 rounded-md sm:w-80 md:min-w-96 max-w-md">

                <h2 className="text-center text-2xl font-bold text-gray-100">Login</h2>

                <Button
                    icon={<FcGoogle />}
                    type="default"
                    className="flex items-center justify-center gap-x-2 mb-5 bg-gray-700 text-gray-100 border-none hover:bg-gray-600"
                    onClick={() => {
                        // Handle Google sign-in logic here
                    }}
                >
                    Sign in with Google
                </Button>

                <div className="relative flex justify-center my-2">
                    <span className="block w-8 h-8 rounded-full border-[1px] border-gray-400
                     text-sm text-gray-400 text-center leading-7 select-none">OR</span>
                </div>

                <label className="flex flex-col gap-y-2">
                    <span>Email</span>
                    <input
                        type="email"
                        name="email"
                        id="email"
                        className="h-10 rounded-md px-2 border border-gray-700 bg-gray-700 text-gray-100 placeholder-gray-400 focus:outline-none focus:ring focus:ring-blue-600"
                        placeholder="Enter your email"
                        required
                    />
                </label>

                <label className="relative flex flex-col gap-y-2">
                    <span>Password</span>
                    <input
                        type={showPassword ? "text" : "password"}
                        name="password"
                        id="password"
                        className="h-10 rounded-md px-2 border border-gray-700 bg-gray-700 text-gray-100 placeholder-gray-400 focus:outline-none focus:ring focus:ring-blue-600"
                        placeholder="Enter your password"
                        required
                    />
                    <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute top-9 right-0 h-8 w-8 cursor-pointer
                        flex justify-center items-center bg-none"
                    >
                        {showPassword ?
                            <HidePasswordIcon fill="black" /> :
                            <ShowPasswordIcon fill="black" />}
                    </button>
                </label>

                <Button
                    type="primary"
                    className="w-full bg-blue-600 hover:bg-blue-500 text-gray-100 border-none"
                >
                    Login
                </Button>

            </form>
        </main>
    )
}
