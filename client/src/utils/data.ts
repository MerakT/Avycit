import { UnauthorizedError, ConflictError } from "@/errors/http_errors";

export async function fetchData(input: RequestInfo, init?: RequestInit) {
    const drf_url = "https://avicyt.onrender.com"
    const response = await fetch( drf_url+input, init);
    if(response.ok){
        return response;
    } else {
        const errorData = await response.json();
        const errorMessage = errorData.error;
    
        if (response.status === 401) {
            throw new UnauthorizedError(errorMessage);
        } else if (response.status === 409) {
            throw new ConflictError(errorMessage);
        } else {
            throw Error(errorMessage);
        }    
    }
}