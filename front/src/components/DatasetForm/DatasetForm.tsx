import React from "react";
import "./styles.scss";

const DatasetForm = (props: {
  selectedDataset: string;
  setSelectedDataset: (value: string) => void;

  renderForm: (formFields: Array<any>) => JSX.Element;
}) => {
  const { selectedDataset, setSelectedDataset, renderForm } = props;

  const staticForm = [
    {
      label: "Dataset",
      value: selectedDataset,
      setValue: (value: string) => setSelectedDataset(value),
      type: "dropdown",
      options: ["RL4SE", "MPM4CPS", "MobileMDE", "LC"],
    },
  ];

  return <>{renderForm(staticForm)}</>;
};

export default DatasetForm;
