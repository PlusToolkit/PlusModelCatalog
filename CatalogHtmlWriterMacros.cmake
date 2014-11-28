MACRO(MODEL_TABLE_START MODEL_TABLE_NAME MODEL_TABLE_DESCRIPTION)
  SET(PAGE_BODY "${PAGE_BODY}
    <h2>${MODEL_TABLE_NAME}</h2>
    <p>${MODEL_TABLE_DESCRIPTION}</p>
    <p>
    <table>
      <thead>
        <tr>
          <th>Image</th>
          <th>ID</td>
          <th>Description</th>
          <th>Printable model</th>
        </tr>
      </thead>
      <tbody>")
ENDMACRO(MODEL_TABLE_START)

MACRO(MODEL_TABLE_ROW)
  set(options "" )
  set(oneValueArgs ID IMAGE_FILE DESCRIPTION EDIT_LINK)
  set(multiValueArgs PRINTABLE_FILES)
  cmake_parse_arguments(MODEL "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )
  
  IF(NOT MODEL_IMAGE_FILE)
    SET(MODEL_IMAGE_FILE "TrackingFixtures/${MODEL_ID}.png")
  ENDIF()
  IF(NOT MODEL_PRINTABLE_FILES)
    SET(MODEL_PRINTABLE_FILES "TrackingFixtures/${MODEL_ID}.stl")
  ENDIF()
    
  IF(NOT MODEL_EDIT_LINK)
    SET(MODEL_EDIT_LINK "https://www.assembla.com/code/plus/subversion/nodes/${Plus_WC_REVISION}/trunk/doc/specifications/TrackingFixtures")
  ENDIF()
  
  FILE(COPY ${CMAKE_CURRENT_SOURCE_DIR}/${MODEL_IMAGE_FILE} DESTINATION "${HTML_OUTPUT_DIR}/rendered")
  FOREACH(MODEL_PRINTABLE_FILE ${MODEL_PRINTABLE_FILES})
    FILE(COPY ${CMAKE_CURRENT_SOURCE_DIR}/${MODEL_PRINTABLE_FILE} DESTINATION "${HTML_OUTPUT_DIR}/printable")
  ENDFOREACH()

  GET_FILENAME_COMPONENT(MODEL_IMAGE_FILE_NAME ${MODEL_IMAGE_FILE} NAME)  
  
  SET(PAGE_BODY "${PAGE_BODY}
          <tr>
          <td><img class=\"model\" src=\"rendered/${MODEL_IMAGE_FILE_NAME}\"></td>
          <td>${MODEL_ID}<br><a href=\"${MODEL_EDIT_LINK}\"><img src=\"link.png\"></a></td>
          <td>${MODEL_DESCRIPTION}</td>  
          <td>")
  FOREACH(MODEL_PRINTABLE_FILE ${MODEL_PRINTABLE_FILES})
    GET_FILENAME_COMPONENT(MODEL_PRINTABLE_FILE_NAME ${MODEL_PRINTABLE_FILE} NAME)
    Subversion_WC_INFO("${CMAKE_CURRENT_SOURCE_DIR}/${MODEL_PRINTABLE_FILE}" PrintableModelFile)
    SET(PRINTABLE_MODEL_REV "${PrintableModelFile_WC_LAST_CHANGED_REV}")
    SET(PAGE_BODY "${PAGE_BODY} <a href=\"printable/${MODEL_PRINTABLE_FILE_NAME}\">${MODEL_PRINTABLE_FILE_NAME}</a> (rev.${PRINTABLE_MODEL_REV})<br>")
  ENDFOREACH()
  SET(PAGE_BODY "${PAGE_BODY} </td>
        </tr>")
        
ENDMACRO(MODEL_TABLE_ROW)

MACRO(MODEL_TABLE_END)
  SET(PAGE_BODY "${PAGE_BODY}
      </tbody>
    </table>")
ENDMACRO(MODEL_TABLE_END)

MACRO(PARAGRAPH TEXT)
  SET(PAGE_BODY
    "${PAGE_BODY} <p>${TEXT}</p>")
ENDMACRO(PARAGRAPH)

MACRO (TODAY RESULT)
    IF (WIN32)
        EXECUTE_PROCESS(COMMAND "cmd" " /C date /T" OUTPUT_VARIABLE ${RESULT})
        string(REGEX REPLACE ".* (..)/(..)/(....).*" "\\1/\\2/\\3" ${RESULT} ${${RESULT}})
    ELSEIF(UNIX)
        EXECUTE_PROCESS(COMMAND "date" "+%d/%m/%Y" OUTPUT_VARIABLE ${RESULT})
        string(REGEX REPLACE "(..)/(..)/(....).*" "\\1/\\2/\\3" ${RESULT} ${${RESULT}})
    ELSE (WIN32)
        MESSAGE(WARNING "date not implemented")
        SET(${RESULT} "unknown")
    ENDIF (WIN32)
ENDMACRO (TODAY)

MACRO(MODEL_CATALOG_START)
  SET(PAGE_BODY "" )
ENDMACRO(MODEL_CATALOG_START)

MACRO(MODEL_CATALOG_END)
  TODAY(CURRENT_DATETIME)
  PARAGRAPH("<br>Generated: ${CURRENT_DATETIME}")
  CONFIGURE_FILE(
    ${CMAKE_CURRENT_SOURCE_DIR}/CatalogTemplate.html.in
    ${HTML_OUTPUT_DIR}/PlusPrintableModelsCatalog.html
    )
  FILE(COPY ${CMAKE_CURRENT_SOURCE_DIR}/link.png DESTINATION "${HTML_OUTPUT_DIR}")
ENDMACRO(MODEL_CATALOG_END)
