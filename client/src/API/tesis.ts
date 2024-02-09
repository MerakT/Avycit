import { fetchData } from "@/utils/data";
import { Tesis } from "@/models/tesis";

export class TesisAPI{
    static async getAllTesis(token: String): Promise<Tesis[]>{
        const response = await fetchData('/api/tesis/',
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token
            },
        });

        const tesisList = await response.json();

        return tesisList;

    }

    static async getTesis(token: String, id: number): Promise<Tesis>{
        const response = await fetchData('/api/tesis/' + id + '/',
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token
            },
        });

        const tesis = await response.json();

        return tesis;
    }

}
