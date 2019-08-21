package errors

func PersistentVolumeNotAvailable() error {
  return &errorString{"Existing Persistent Volume is currently not Available: Could still be terminating"}
}

type errorString struct {
  text string
}

func (e *errorString) Error() string {
  return e.text
}
