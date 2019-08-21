package v1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EDIT THIS FILE!  THIS IS SCAFFOLDING FOR YOU TO OWN!
// NOTE: json tags are required.  Any new fields you add must have json tags for the fields to be serialized.

// KrmRedisSpec defines the desired state of KrmRedis
// +k8s:openapi-gen=true
type KrmRedisSpec struct {
	NodeSelector map[string]string `json:"nodeSelector"`
	RedisSecret string `json:"redisSecret"`
	StorageSpec KrmStorageSpec `json:"storageSpec"`
}

// KrmRedisStatus defines the observed state of KrmRedis
// +k8s:openapi-gen=true
type KrmRedisStatus struct {
	Status metav1.Status `json:"status"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// KrmRedis is the Schema for the krmredis API
// +k8s:openapi-gen=true
// +kubebuilder:subresource:status
type KrmRedis struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   KrmRedisSpec   `json:"spec,omitempty"`
	Status KrmRedisStatus `json:"status,omitempty"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// KrmRedisList contains a list of KrmRedis
type KrmRedisList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []KrmRedis `json:"items"`
}

func init() {
	SchemeBuilder.Register(&KrmRedis{}, &KrmRedisList{})
}
