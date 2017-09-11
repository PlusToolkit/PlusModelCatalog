PROJECT(PlusModelCatalog)
CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

# ------------------------------------------------------------------------
# Find Plus use file
IF ( NOT PLUSLIB_DIR )
    FIND_PACKAGE (PlusLib)
ELSE ()
    FIND_PACKAGE (PlusLib REQUIRED PATHS "${PLUSLIB_DIR}/src" NO_DEFAULT_PATH)
ENDIF() 

IF ( PlusLib_FOUND)
  INCLUDE( ${PlusLib_USE_FILE} )
ELSE( PlusLib_FOUND )
    MESSAGE( FATAL_ERROR "This project requires PlusLib for generating rendering images of STL model files. Please verify configuration.")
ENDIF( PlusLib_FOUND )

SET(PlusModelCatalog_REVISION "NA")
SET(PlusModelCatalog_SHORT_REVISION "NA")
FUNCTION(GIT_LAST_CHANGED_TAG filename outputVarName)
  set(outputVarName "NA" PARENT_SCOPE)
ENDFUNCTION()

IF(NOT PLUS_OFFLINE_BUILD)
  # Need git for the automatic update of the repository
  FIND_PACKAGE(Git)
  IF(Git_FOUND)
    EXECUTE_PROCESS(COMMAND "${GIT_EXECUTABLE}" rev-parse HEAD 
      OUTPUT_VARIABLE PlusModelCatalog_REVISION 
      WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
      )
    STRING(REGEX REPLACE "\n$" "" PlusModelCatalog_REVISION "${PlusModelCatalog_REVISION}")
    STRING(REGEX REPLACE "\r$" "" PlusModelCatalog_REVISION "${PlusModelCatalog_REVISION}")
    
    MESSAGE(STATUS "Current git hash is ${PlusModelCatalog_REVISION}")

    EXECUTE_PROCESS(COMMAND "${GIT_EXECUTABLE}" rev-parse --short HEAD 
      OUTPUT_VARIABLE PlusModelCatalog_SHORT_REVISION 
      WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
      )
    STRING(REGEX REPLACE "\n$" "" PlusModelCatalog_SHORT_REVISION "${PlusModelCatalog_SHORT_REVISION}")
    STRING(REGEX REPLACE "\r$" "" PlusModelCatalog_SHORT_REVISION "${PlusModelCatalog_SHORT_REVISION}")

    FUNCTION(GIT_LAST_CHANGED_TAG filename outputVarName)
      EXECUTE_PROCESS(COMMAND "${GIT_EXECUTABLE}" log -n 1 --date=short --pretty=format:%ad-%h -- ${filename}
        OUTPUT_VARIABLE gitTag
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        )
      STRING(REGEX REPLACE "\n$" "" gitTag "${gitTag}")
      STRING(REGEX REPLACE "\r$" "" gitTag "${gitTag}")
      SET(${outputVarName} ${gitTag} PARENT_SCOPE)
    ENDFUNCTION()

  ELSE()
    MESSAGE(WARNING "Git tool not found. Cannot retrieve revision information from repository")
  ENDIF()
ENDIF()

SET(CATALOG_URL "https://github.com/PlusToolkit/PlusModelCatalog/tree/${PlusModelCatalog_REVISION}")
SET(HTML_OUTPUT_DIR "${CMAKE_CURRENT_BINARY_DIR}/html")

INCLUDE(CatalogHtmlWriterMacros.cmake)
INCLUDE(CatalogContents.cmake)

# The solution has to be re-built each time when the contents is modified,
# create a convenience batch file that performs this.
STRING(TOUPPER ${CMAKE_MAKE_PROGRAM} MAKE_PROGRAM_UPPERCASE)
IF (${MAKE_PROGRAM_UPPERCASE} MATCHES "MSBUILD")
  SET(IS_MAKE_PROGRAM_MSBUILD TRUE)
ELSE()
  SET(IS_MAKE_PROGRAM_MSBUILD FALSE)
ENDIF()
CONFIGURE_FILE(
  CreateModelCatalog.bat.in
  ${CMAKE_CURRENT_BINARY_DIR}/CreateModelCatalog.bat
  )
# Batch file for build with dashboard submission
configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/BuildAndTest.bat.in 
  ${CMAKE_CURRENT_BINARY_DIR}/BuildAndTest.bat
  )

# --------------------------------------------------------------------------
# Testing
#

# Required for dashboard submission  
INCLUDE(CTest)