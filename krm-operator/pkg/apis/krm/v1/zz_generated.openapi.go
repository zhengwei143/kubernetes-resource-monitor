// +build !ignore_autogenerated

// This file was autogenerated by openapi-gen. Do not edit it manually!

package v1

import (
	spec "github.com/go-openapi/spec"
	common "k8s.io/kube-openapi/pkg/common"
)

func GetOpenAPIDefinitions(ref common.ReferenceCallback) map[string]common.OpenAPIDefinition {
	return map[string]common.OpenAPIDefinition{
		"kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmRedis":         schema_pkg_apis_krm_v1_KrmRedis(ref),
		"kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmRedisSpec":     schema_pkg_apis_krm_v1_KrmRedisSpec(ref),
		"kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmRedisStatus":   schema_pkg_apis_krm_v1_KrmRedisStatus(ref),
		"kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmWatcher":       schema_pkg_apis_krm_v1_KrmWatcher(ref),
		"kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmWatcherSpec":   schema_pkg_apis_krm_v1_KrmWatcherSpec(ref),
		"kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmWatcherStatus": schema_pkg_apis_krm_v1_KrmWatcherStatus(ref),
	}
}

func schema_pkg_apis_krm_v1_KrmRedis(ref common.ReferenceCallback) common.OpenAPIDefinition {
	return common.OpenAPIDefinition{
		Schema: spec.Schema{
			SchemaProps: spec.SchemaProps{
				Description: "KrmRedis is the Schema for the krmredis API",
				Properties: map[string]spec.Schema{
					"kind": {
						SchemaProps: spec.SchemaProps{
							Description: "Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds",
							Type:        []string{"string"},
							Format:      "",
						},
					},
					"apiVersion": {
						SchemaProps: spec.SchemaProps{
							Description: "APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#resources",
							Type:        []string{"string"},
							Format:      "",
						},
					},
					"metadata": {
						SchemaProps: spec.SchemaProps{
							Ref: ref("k8s.io/apimachinery/pkg/apis/meta/v1.ObjectMeta"),
						},
					},
					"spec": {
						SchemaProps: spec.SchemaProps{
							Ref: ref("kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmRedisSpec"),
						},
					},
					"status": {
						SchemaProps: spec.SchemaProps{
							Ref: ref("kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmRedisStatus"),
						},
					},
				},
			},
		},
		Dependencies: []string{
			"k8s.io/apimachinery/pkg/apis/meta/v1.ObjectMeta", "kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmRedisSpec", "kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmRedisStatus"},
	}
}

func schema_pkg_apis_krm_v1_KrmRedisSpec(ref common.ReferenceCallback) common.OpenAPIDefinition {
	return common.OpenAPIDefinition{
		Schema: spec.Schema{
			SchemaProps: spec.SchemaProps{
				Description: "KrmRedisSpec defines the desired state of KrmRedis",
				Properties:  map[string]spec.Schema{},
			},
		},
		Dependencies: []string{},
	}
}

func schema_pkg_apis_krm_v1_KrmRedisStatus(ref common.ReferenceCallback) common.OpenAPIDefinition {
	return common.OpenAPIDefinition{
		Schema: spec.Schema{
			SchemaProps: spec.SchemaProps{
				Description: "KrmRedisStatus defines the observed state of KrmRedis",
				Properties:  map[string]spec.Schema{},
			},
		},
		Dependencies: []string{},
	}
}

func schema_pkg_apis_krm_v1_KrmWatcher(ref common.ReferenceCallback) common.OpenAPIDefinition {
	return common.OpenAPIDefinition{
		Schema: spec.Schema{
			SchemaProps: spec.SchemaProps{
				Description: "KrmWatcher is the Schema for the krmwatchers API",
				Properties: map[string]spec.Schema{
					"kind": {
						SchemaProps: spec.SchemaProps{
							Description: "Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds",
							Type:        []string{"string"},
							Format:      "",
						},
					},
					"apiVersion": {
						SchemaProps: spec.SchemaProps{
							Description: "APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#resources",
							Type:        []string{"string"},
							Format:      "",
						},
					},
					"metadata": {
						SchemaProps: spec.SchemaProps{
							Ref: ref("k8s.io/apimachinery/pkg/apis/meta/v1.ObjectMeta"),
						},
					},
					"spec": {
						SchemaProps: spec.SchemaProps{
							Ref: ref("kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmWatcherSpec"),
						},
					},
					"status": {
						SchemaProps: spec.SchemaProps{
							Ref: ref("kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmWatcherStatus"),
						},
					},
				},
			},
		},
		Dependencies: []string{
			"k8s.io/apimachinery/pkg/apis/meta/v1.ObjectMeta", "kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmWatcherSpec", "kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1.KrmWatcherStatus"},
	}
}

func schema_pkg_apis_krm_v1_KrmWatcherSpec(ref common.ReferenceCallback) common.OpenAPIDefinition {
	return common.OpenAPIDefinition{
		Schema: spec.Schema{
			SchemaProps: spec.SchemaProps{
				Description: "KrmWatcherSpec defines the desired state of KrmWatcher",
				Properties: map[string]spec.Schema{
					"image": {
						SchemaProps: spec.SchemaProps{
							Type:   []string{"string"},
							Format: "",
						},
					},
					"namespace": {
						SchemaProps: spec.SchemaProps{
							Type:   []string{"string"},
							Format: "",
						},
					},
					"verificationWaitDuration": {
						SchemaProps: spec.SchemaProps{
							Type:   []string{"integer"},
							Format: "int64",
						},
					},
					"aggregationWaitDuration": {
						SchemaProps: spec.SchemaProps{
							Type:   []string{"integer"},
							Format: "int64",
						},
					},
					"watchingResource": {
						SchemaProps: spec.SchemaProps{
							Type:   []string{"string"},
							Format: "",
						},
					},
				},
				Required: []string{"image", "namespace", "verificationWaitDuration", "aggregationWaitDuration", "watchingResource"},
			},
		},
		Dependencies: []string{},
	}
}

func schema_pkg_apis_krm_v1_KrmWatcherStatus(ref common.ReferenceCallback) common.OpenAPIDefinition {
	return common.OpenAPIDefinition{
		Schema: spec.Schema{
			SchemaProps: spec.SchemaProps{
				Description: "KrmWatcherStatus defines the observed state of KrmWatcher",
				Properties: map[string]spec.Schema{
					"streamerStatus": {
						SchemaProps: spec.SchemaProps{
							Ref: ref("k8s.io/apimachinery/pkg/apis/meta/v1.Status"),
						},
					},
					"verifierStatus": {
						SchemaProps: spec.SchemaProps{
							Ref: ref("k8s.io/apimachinery/pkg/apis/meta/v1.Status"),
						},
					},
					"aggregatorStatus": {
						SchemaProps: spec.SchemaProps{
							Ref: ref("k8s.io/apimachinery/pkg/apis/meta/v1.Status"),
						},
					},
				},
				Required: []string{"streamerStatus", "verifierStatus", "aggregatorStatus"},
			},
		},
		Dependencies: []string{
			"k8s.io/apimachinery/pkg/apis/meta/v1.Status"},
	}
}