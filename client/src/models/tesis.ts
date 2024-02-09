import { User } from "./user";

export interface Tesis {
    id: number;
    title: string;
    area: string;
    student: User;
    advisor: User;
    judge_1: User;
    judge_2: User;
    judge_3: User;
    start_date: string;
    status: string;
}

export interface Observacion {
    id: number;
    tesis: Tesis;
    written_by: User;
    description: string;
}