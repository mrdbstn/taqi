import { useEffect, useState } from "react";



export default function Home() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetch("http://127.0.0.1:8000/main")
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  return (
    <div className="h-screen w-screen bg-gradient-to-tl from-gray-900 to-gray-600 flex flex-row items-center justify-center">
      <div className=" w-2/3 h-full text-white flex flex-col items-center">
        <h1 className="text-7xl font-bold flex flex-col items-center p-16">
          Upload your profiles
        </h1>
        <h2 className=""> Server test: {data.message}</h2>
      </div>
    </div>
  );
}
