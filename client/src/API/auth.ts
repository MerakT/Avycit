import { fetchData } from "@/utils/data";
import { User } from "@/models/user";
import { LoginBody } from "@/interfaces/auth";

export class AuthAPI{
    static async getLoggedInUser(token: String): Promise<User>{

        const response = await fetchData('/api/authuser/',
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token

            },
        });

        const user = await response.json();

        return user;
    }

    static async login(body: LoginBody): Promise<User>{
        const response = await fetchData('/api/authlogin',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });

        const token = await response.json();

        // Save the token and role in local storage
        localStorage.setItem('token', token);
        localStorage.setItem('role', token.user.role);

        // Get the user data
        const user = await this.getLoggedInUser(token); 
        console.log(user.role);

        return user;
    }

    static async logout(): Promise<void>{
        const token = localStorage.getItem('token');

        await fetchData('/api/authlogout',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token
            }
        });

        // Remove the token and role from local storage
        localStorage.removeItem('token');
        localStorage.removeItem('role');
    }
}