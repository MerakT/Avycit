import { Tesis } from "@/models/tesis";

interface TesistaListaProps {
    tesis: Tesis[];
}

export default function TesistasLista({tesis}: TesistaListaProps) {
    tesis.map((tesis) => {
        return (
            <div key={tesis.id}>
                <h2>{tesis.title}</h2>
                <p>{String(tesis.student)}</p>
                <p>{String(tesis.advisor)}</p>
                <p>{tesis.status}</p>
            </div>
        )
    })
}