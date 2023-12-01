import Link from "next/link";
import { useEffect, useState } from "react";

const ProfileView = ({ profile }) => {
  return (
    <div className="flex flex-col items-center justify-center space-y-2">
      <div className="flex flex-col items-start justify-center space-y-2">
        <h2 className="text-sm font-medium">
          {profile}
        </h2>
      </div>
    </div>
  );
};


const ProfileContainer = ({ title, profiles }) => {
  return (
    <div className="flex flex-col items-center justify-center space-y-2 border-2 border-white p-4 rounded-md">
      <h1 className="text-2xl font-bold">{title}</h1>
      <div className="flex flex-col items-start justify-start space-y-2 h-52 w-full overflow-y-auto ">
        {profiles?.map((profile) => (
          <ProfileView profile={profile} />
          
        ))}
      </div>
    </div>
  );
};


const ServerTest = () => {
  const [serverTest, setServerTest] = useState(null);
  useEffect(() => {
    fetch("http://127.0.0.1:8000/main")
      .then((response) => response.json())
      .then((data) => setServerTest(data));
  }, []);

  const status = serverTest ? true : false;

  return (
    <div className="flex flex-row justify-center items-center space-x-2">
      <div>
        <div
          className={`w-4 h-4 rounded-full ${
            status ? "bg-green-500" : "bg-red-500"
          } animate-pulse`}
        ></div>
      </div>
      <h1 className="text-xl ">
        Backend is {status ? "connected" : "not connected"}
      </h1>
    </div>
  );
};

export default function Home() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);

  const uploadFile = () => {
    const formData = new FormData();
    formData.append("spreadsheet", file);
    fetch("http://127.0.0.1:8000/main/process_csv/", {
      method: "POST",
      contentType: "multipart/form-data",
      body: formData,
    })
      .then((response) => response.json())
      .then((serverData) => {
        let { data } = serverData;
        setData(data);
      });
  };

  return (
    <div className="h-screen w-screen bg-black flex flex-col text-white">
      <div className="p-8 flex flex-row justify-between">
        <ServerTest />
      </div>
      <div className="flex flex-row flex-grow items-center justify-center">
        <div className="w-1/2 flex flex-col items-center justify-center p-16 space-y-6 text-white ">
          <div className="flex flex-col items-center space-y-2">
            <h1 className="text-7xl font-bold flex flex-col items-center">
              Upload your profiles
            </h1>
            <h2 className="text-xl font-medium">
              Generate profiles for your users based on your spreadsheet data
            </h2>
          </div>
          <div className="flex flex-col items-center justify-center space-y-2">
            <div>
              <input
                type="file"
                name="file"
                className="bg-white p-2 rounded-s-md text-black"
                onChange={(e) => setFile(e.target.files[0])}
              />
              <button
                type="button"
                className="bg-blue-600 p-[0.69rem] rounded-e-md"
                onClick={uploadFile}
              >
                Upload
              </button>
            </div>
            {data && (
              <div className="flex flex-col items-center justify-center space-y-2">
                <h1 className="text-2xl font-bold">Results</h1>
                <div className="flex flex-col items-center justify-center space-y-2">
                  <h2 className="text-xl font-medium">
                    Total profiles generated: {data.new}
                  </h2>
                  <h2 className="text-xl font-medium">
                    Already existing profiles: {data.existing}
                  </h2>
                  <h2 className="text-xl font-medium">
                    Total profiles with errors: {data.errors}
                  </h2>
                  <div className="flex flex-row space-x-2">
                    <ProfileContainer title="New profiles" profiles={data.new_users} />
                    <ProfileContainer title="Existing profiles" profiles={data.existing_users} />
                    <ProfileContainer title="Profiles with errors" profiles={data.error_rows} />
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
