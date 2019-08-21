package v1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EDIT THIS FILE!  THIS IS SCAFFOLDING FOR YOU TO OWN!
// NOTE: json tags are required.  Any new fields you add must have json tags for the fields to be serialized.

// KrmWatcherSpec defines the desired state of KrmWatcher
// +k8s:openapi-gen=true
type KrmWatcherSpec struct {
	Image string `json:"image"`
	NodeSelector map[string]string `json:"nodeSelector"`
	VerificationWaitDuration int64 `json:"verificationWaitDuration"`
	AggregationWaitDuration int64 `json:"aggregationWaitDuration"`
	WatchingResource string `json:"watchingResource"`
}

// KrmWatcherStatus defines the observed state of KrmWatcher
// +k8s:openapi-gen=true
type KrmWatcherStatus struct {
	StreamerStatus metav1.Status `json:"streamerStatus"`
	VerifierStatus metav1.Status `json:"verifierStatus"`
	AggregatorStatus metav1.Status `json:"aggregatorStatus"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// KrmWatcher is the Schema for the krmwatchers API
// +k8s:openapi-gen=true
// +kubebuilder:subresource:status
type KrmWatcher struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   KrmWatcherSpec   `json:"spec,omitempty"`
	Status KrmWatcherStatus `json:"status,omitempty"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// KrmWatcherList contains a list of KrmWatcher
type KrmWatcherList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []KrmWatcher `json:"items"`
}

func init() {
	SchemeBuilder.Register(&KrmWatcher{}, &KrmWatcherList{})
}
