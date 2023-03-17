import { useState, useEffect } from "react";

interface DataType {
  data: any;
}

function useFetch(url: string): [DataType | null, boolean, Error | null] {
  const [data, setData] = useState<DataType | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function fetchData() {
      setIsLoading(true);

      try {
        const response = await fetch(url);
        const data = await response.json();
        setData(data);
      } catch (error) {
        // @ts-ignore
        setError(error);
      }

      setIsLoading(false);
    }

    fetchData();
  }, [url]);

  return [data, isLoading, error];
}

export default useFetch;
