import { UnauthorizedError, ConflictError } from "@/errors/http_errors";

export async function fetchData(input: RequestInfo, init?: RequestInit) {
    const baseURL = "http://127.0.0.1:8000/";
    const authorizationToken = "Token d854000a3ab4a1b1242e3c22573058ca7420eddf";

    const updatedInit: RequestInit = {
        ...init,
        headers: {
            ...init?.headers,
            Authorization: authorizationToken
        }
    };

    const response = await fetch(baseURL + input, updatedInit);
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
