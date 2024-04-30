import React, { useEffect, useState } from "react";
import "./styles.scss";

const ResultsPage = (props: { projectId: string }) => {
  const { projectId } = props;

  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [metrics, setMetrics] = useState<Object>({});

  // const data = {
  //   accuracy: 0.5007332205301749,
  //   precision: 0.09170208007157235,
  //   recall: 0.5290322580645161,
  //   f1_score: 0.1563095691955776,
  //   specificity: 0.4980222496909765,
  //   mcc: 0.5076419183245933,
  //   balanced_accuracy: 0.5135272538777463,
  //   miss_rate: 0.47096774193548385,
  //   fb_score: 0.2707700435873729,
  //   wss: 0.02468933646271132,
  //   "wss@95": 0.44565707839819513,
  //   npv: 0.9169321802457897,
  //   g_mean: 0.5132931280665928,
  // };

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
        setMetrics(resjson);
      })
      .catch((error: string) => {
        setIsLoading(false);
        setIsError(true);
        console.log("Final ERROR :", error);
      });
  };

  return (
    <div className="results-container">
      {isLoading ? (
        <div>Please Wait...</div>
      ) : isError ? (
        <div className="results-error">An Error Occured !!</div>
      ) : (
        <>
          <p className="results-title">Performance Metrics</p>
          <div className="results-box">
            {Object.entries(metrics).map(([key, value]) => (
              <ul key={key}>
                <li>
                  <span className={"results-box_key"}>{key}</span>:
                  <span className={"results-box_value"}>{value}</span>
                </li>
              </ul>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default ResultsPage;
