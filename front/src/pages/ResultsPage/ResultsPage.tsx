import React from "react";
import "./styles.scss";

const ResultsPage = () => {
  const data = {
    accuracy: 0.233344354,
    precision: 0.45453432,
    recall: 0.435436433,
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
            {key}: {value}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResultsPage;
