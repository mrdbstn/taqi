import { useEffect } from "react";

export default function Home() {
  useEffect(() => {
    fetch("http://127.0.0.1:8000/main")
      .then((response) => response.json())
      .then((data) => console.log(data))
  }, []);

  return <div className="h-screen w-screen bg-black text-white">yo</div>;
}
