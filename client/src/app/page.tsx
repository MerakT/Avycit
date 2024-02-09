import Image from "next/image";
import { AuthAPI } from "@/API/auth";
import { User as UserModel } from "@/models/user";
import { getToken } from "@/API/session";

export default function Home() {
  const token = getToken()


  return (
    <main>
    </main>
  );
}
