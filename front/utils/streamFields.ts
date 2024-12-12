export const getStreamFieldStructMediaWithUrl = (
  initialData,
  objectType,
  listObjectWithUrl,
) => {
  /**
   * StreamFieldStructure : StreamField(StructBlock({.., objectType: id}))
   * objectType can be image, svg or document
   */
  const streamFieldString = initialData
  const dataToReturn = []
  for (const item of JSON.parse(streamFieldString)) {
    dataToReturn.push({
      ...item.value,
      [objectType + "Url"]: listObjectWithUrl.filter(
        (object) => object.id === item.value[objectType],
      )[0].url,
    })
  }
  return dataToReturn
}

export const getStreamFieldMediaWithUrl = (
  initialData,
  objectType,
  listObjectWithUrl,
) => {
  /**
   * StreamFieldStructure : StreamField({..}, {type: objectType, value: id})
   * objectType can be image, svg or document
   */
  const streamFieldString = initialData
  const dataToReturn = []
  for (const item of JSON.parse(streamFieldString)) {
    if (item.type === objectType) {
      dataToReturn.push({
        ...item,
        [objectType + "Url"]: listObjectWithUrl.filter(
          (object) => object.id === item.value,
        )[0].url,
      })
    } else {
      dataToReturn.push({
        ...item,
      })
    }
  }
  return dataToReturn
}

export const getStreamFieldStructWithLinkedObject = (
  initialData,
  streamFieldAtribut,
  listObject,
  objectAttribut,
) => {
  /**
   * StreamFieldStructure : StreamField(StructBlock({.., streamFieldAtribut: id | string}))
   */
  const streamFieldString = initialData
  const dataToReturn = []
  for (const item of JSON.parse(streamFieldString)) {
    dataToReturn.push({
      ...item.value,
      ...listObject.filter(
        (object) => object[objectAttribut] === item.value[streamFieldAtribut],
      )[0],
    })
  }
  return dataToReturn
}

export const getStreamFieldStructWithListLinkedObjects = (
  initialData,
  streamFieldListName,
  listObject,
  objectAttribut,
) => {
  /**
   * StreamFieldStructure : StreamField(StructBlock(ListBlock(ObjectToLinked: {value: id})))
   */
  const streamFieldString = initialData
  const dataToReturn = []
  for (const firstLevelItem of JSON.parse(streamFieldString)) {
    const secondLevelItemToReturn = []
    for (const secondLevelItem of firstLevelItem.value[streamFieldListName]) {
      secondLevelItemToReturn.push({
        ...secondLevelItem.value,
        ...listObject.filter(
          (object) => object[objectAttribut] === secondLevelItem.value,
        )[0],
      })
    }
    dataToReturn.push({
      ...firstLevelItem.value,
      [streamFieldListName]: secondLevelItemToReturn,
    })
  }
  return dataToReturn
}

export const getStreamFieldListStructMediaWithUrl = (
  initialData,
  streamFieldListName,
  objectType,
  listObjectWithUrl,
) => {
  /**
   * StreamFieldStructure : StreamField({..}, {type: streamFieldListName, value: listBlock(StructBlock({.., objectType: id}))})
   */
  const streamFieldString = initialData
  const dataToReturn = []
  for (const firstLevelItem of JSON.parse(streamFieldString)) {
    const secondLevelItemToReturn = []
    if (firstLevelItem.type === streamFieldListName) {
      for (const secondLevelItem of firstLevelItem.value) {
        const correspondingItems = listObjectWithUrl.filter(
          (object) => object.id === secondLevelItem.value[objectType],
        )
        const url = correspondingItems.length ? correspondingItems[0].url : null
        secondLevelItemToReturn.push({
          ...secondLevelItem.value,
          [objectType + "Url"]: url,
        })
      }
      dataToReturn.push({
        ...firstLevelItem,
        value: secondLevelItemToReturn,
      })
    } else {
      dataToReturn.push({
        ...firstLevelItem,
      })
    }
  }
  return dataToReturn
}
