import React from "react";
import "./styles.scss";

const ProjectInfoForm = (props: {
  projectName: string;
  setProjectName: (value: string) => void;
  topicTitle: string;
  setTopicTitle: (value: string) => void;
  topicDescription: string;
  setTopicDescription: (value: string) => void;
  renderForm: (formFields: Array<any>, className?: string) => JSX.Element;
}) => {
  const {
    projectName,
    setProjectName,
    topicTitle,
    setTopicTitle,
    topicDescription,
    setTopicDescription,
    renderForm,
  } = props;

  const formData = [
    {
      label: "Name",
      value: projectName,
      setValue: setProjectName,
      type: "textInput",
      props: {
        placeholder: "myproject",
      },
    },
    {
      label: "topic title",
      value: topicTitle,
      setValue: setTopicTitle,
      type: "textInput",
      props: {
        placeholder: "RL4SE",
      },
    },
    {
      label: "topic description",
      value: topicDescription,
      setValue: setTopicDescription,
      type: "textInput",
      props: {
        placeholder: "reinforcement learning for software engineering",
      },
    },
  ];
  return <>{renderForm(formData)}</>;
};

export default ProjectInfoForm;
