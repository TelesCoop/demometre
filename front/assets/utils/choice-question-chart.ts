function getLeftValue(
  index: number,
  percentageOfSpaceAlreadyTaken: number,
  totalLine: number,
): number {
  return (
    percentageOfSpaceAlreadyTaken +
    ((1 - percentageOfSpaceAlreadyTaken) * index) / (totalLine - 1)
  )
}

export function getLeftStyle(
  index: number,
  percentageOfSpaceAlreadyTaken: number,
  totalLine: number,
  gapSize: number,
  percentageSize: number,
  leftBaseMargin = 1,
): string {
  const leftValue = getLeftValue(
    index,
    percentageOfSpaceAlreadyTaken,
    totalLine,
  )
  return `left: calc((100% - ${gapSize}rem - ${percentageSize}px) * ${leftValue} + ${leftBaseMargin}rem)`
}

export function getColorGradients(color: string) {
  const toReturn = {
    1: [[`${color}-dark`, "white"]],
    2: [
      [`${color}-light-active`, `${color}-dark`],
      [`${color}-dark`, "white"],
    ],
    3: [
      [`${color}-light-active`, `${color}-dark`],
      [`${color}`, `${color}-dark`],
      [`${color}-dark`, "white"],
    ],
    4: [
      [`${color}-light-active`, `${color}-dark`],
      [`${color}`, `${color}-dark`],
      [`${color}-hover`, "white"],
      [`${color}-dark`, "white"],
    ],
    5: [
      [`${color}-light-active`, `${color}-dark`],
      [`${color}`, `${color}-dark`],
      [`${color}-hover`, "white"],
      [`${color}-active`, "white"],
      [`${color}-dark`, "white"],
    ],
    6: [
      [`${color}-light-active`, `${color}-dark`],
      [`${color}`, `${color}-dark`],
      [`${color}-hover`, "white"],
      [`${color}-active`, "white"],
      [`${color}-dark`, "white"],
      [`${color}-light-active`, `${color}-dark`],
    ],
  }
  toReturn[7] = [...toReturn[6], ...toReturn[6].slice(0, 1)]
  toReturn[8] = [...toReturn[6], ...toReturn[6].slice(0, 2)]
  toReturn[9] = [...toReturn[6], ...toReturn[6].slice(0, 3)]
  toReturn[10] = [...toReturn[6], ...toReturn[6].slice(0, 4)]
  toReturn[11] = [...toReturn[6], ...toReturn[6].slice(0, 5)]
  toReturn[12] = [...toReturn[6], ...toReturn[6].slice(0, 6)]
  return toReturn
}
