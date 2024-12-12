export const getPercentage = (value: number, total: number) => {
  return total ? Math.round((value / total) * 100) : 0
}
