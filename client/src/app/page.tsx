import Image from "next/image";
import { AuthAPI } from "@/API/auth";
import { User as UserModel } from "@/models/user";
import { getToken } from "@/API/session";

export default function Home() {
  const getUser = async () => {
    const token = await getToken();
    if (token == null) {
      return;
    }
    const user = AuthAPI.getLoggedInUser(token);
  };

  getUser();

  return (
    <main>
    </main>
  );
}
