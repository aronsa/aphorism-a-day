fetch("./aphorism.json")
  .then((response) => response.json())
  .then((data) => {
    // Update the aphorism text
    const aphorismElement = document.querySelector(".aphorism");
    aphorismElement.textContent = `"${data.aphorism.trim()}"`;
    console.log("setting text as:");
    console.log(data.aphorism.trim());
    // Update the number
    const numberElement = document.querySelector(".number");
    numberElement.textContent = data.number;

    // Update the work title
    const workElement = document.querySelector(".work");
    workElement.textContent = data.work;

    // Update the work link
    const workLinkElement = document.querySelector(".work-link");
    workLinkElement.href = data.workLink;
    workLinkElement.textContent = data.work;
    workElement.replaceWith(workLinkElement);
  })
  .catch((error) => {
    console.error("Error fetching data:", error);
    document.querySelector(".aphorism").textContent =
      "Apologies, but it appears there's been an issue retreiving today's aphorism. If this continues to be an issue, drop Sam a line.";
  });
