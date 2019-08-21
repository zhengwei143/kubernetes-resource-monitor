package v1

import (
  "k8s.io/apimachinery/pkg/api/resource"
  corev1 "k8s.io/api/core/v1"
)

type KrmStorageSpec struct {
  HostPath corev1.HostPathVolumeSource `json:"hostPath"`
  Storage resource.Quantity `json:"storage"`
  AccessModes []corev1.PersistentVolumeAccessMode `json:"accessModes"`
}
