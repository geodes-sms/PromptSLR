import React, { useEffect, useState } from "react";
import "./styles.scss";

const ResultsPage = (props: { projectId: string }) => {
  const { projectId } = props;

  const [isLoading, setIsLoading] = useState(true);

  const data = {
    accuracy: 0.233344354,
    precision: 0.45453432,
    recall: 0.435436433,
  };

  useEffect(() => {
    setTimeout(() => {
      onRequestResult();
    }, 10000);
  }, []);

  const onRequestResult = () => {
    fetch(`http://localhost:8000/experiment/results/${projectId}`,{headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    }})
      .then((response) => response.json())
      .then((resjson) => {
        setIsLoading(false);
        console.log(console.log("FINAL RESPONSE :", resjson));
      })
      .catch((error: string) => {
        setIsLoading(false);
        console.log("Final ERROR :", error);
      });
  };

  //   const papers = [
  //     {
  //       title: "",
  //       abstract: "",
  //     },
  //   ];
  return (
    <div className="results-container">
      <p className="results-title">Performance Metrics</p>
      <div className="results-box">
        {Object.entries(data).map(([key, value]) => (
          <div key={key}>
            <span>{key}</span>:<span>{value}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResultsPage;
