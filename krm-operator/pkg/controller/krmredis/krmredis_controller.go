package krmredis

import (
	"time"
	"context"

	krmv1 "github.com/zhengwei143/kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1"
	ctrlerrors "github.com/zhengwei143/kubernetes-resource-monitor/krm-operator/pkg/controller/errors"
	"github.com/go-logr/logr"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
  "k8s.io/apimachinery/pkg/api/resource"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	extv1beta1 "k8s.io/api/extensions/v1beta1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/controller"
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
	"sigs.k8s.io/controller-runtime/pkg/handler"
	"sigs.k8s.io/controller-runtime/pkg/manager"
	"sigs.k8s.io/controller-runtime/pkg/reconcile"
	logf "sigs.k8s.io/controller-runtime/pkg/runtime/log"
	"sigs.k8s.io/controller-runtime/pkg/source"
)

var log = logf.Log.WithName("controller_krmredis")

/**
* USER ACTION REQUIRED: This is a scaffold file intended for the user to modify with their own Controller
* business logic.  Delete these comments after modifying this file.*
 */

// Add creates a new KrmRedis Controller and adds it to the Manager. The Manager will set fields on the Controller
// and Start it when the Manager is Started.
func Add(mgr manager.Manager) error {
	return add(mgr, newReconciler(mgr))
}

// newReconciler returns a new reconcile.Reconciler
func newReconciler(mgr manager.Manager) reconcile.Reconciler {
	return &ReconcileKrmRedis{client: mgr.GetClient(), scheme: mgr.GetScheme()}
}

// add adds a new Controller to mgr with r as the reconcile.Reconciler
func add(mgr manager.Manager, r reconcile.Reconciler) error {
	// Create a new controller
	c, err := controller.New("krmredis-controller", mgr, controller.Options{Reconciler: r})
	if err != nil {
		return err
	}

	// Watch for changes to primary resource KrmRedis
	err = c.Watch(&source.Kind{Type: &krmv1.KrmRedis{}}, &handler.EnqueueRequestForObject{})
	if err != nil {
		return err
	}

	// err = c.Watch(&source.Kind{Type: &corev1.PersistentVolume{}}, &handler.EnqueueRequestForOwner{
	// 	IsController: true,
	// 	OwnerType:    &krmv1.KrmRedis{},
	// })
	// if err != nil {
	// 	return err
	// }
	//
	// err = c.Watch(&source.Kind{Type: &corev1.PersistentVolumeClaim{}}, &handler.EnqueueRequestForOwner{
	// 	IsController: true,
	// 	OwnerType:    &krmv1.KrmRedis{},
	// })
	// if err != nil {
	// 	return err
	// }
	//
	// err = c.Watch(&source.Kind{Type: &extv1beta1.Deployment{}}, &handler.EnqueueRequestForOwner{
	// 	IsController: true,
	// 	OwnerType:    &krmv1.KrmRedis{},
	// })
	// if err != nil {
	// 	return err
	// }
	//
	// err = c.Watch(&source.Kind{Type: &corev1.Service{}}, &handler.EnqueueRequestForOwner{
	// 	IsController: true,
	// 	OwnerType:    &krmv1.KrmRedis{},
	// })
	// if err != nil {
	// 	return err
	// }

	return nil
}

// blank assignment to verify that ReconcileKrmRedis implements reconcile.Reconciler
var _ reconcile.Reconciler = &ReconcileKrmRedis{}

// ReconcileKrmRedis reconciles a KrmRedis object
type ReconcileKrmRedis struct {
	// This client, initialized using mgr.Client() above, is a split client
	// that reads objects from the cache and writes to the apiserver
	client client.Client
	scheme *runtime.Scheme
}



// Reconcile reads that state of the cluster for a KrmRedis object and makes changes based on the state read
// and what is in the KrmRedis.Spec
// Note:
// The Controller will requeue the Request to be processed again if the returned error is non-nil or
// Result.Requeue is true, otherwise upon completion it will remove the work from the queue.
func (r *ReconcileKrmRedis) Reconcile(request reconcile.Request) (reconcile.Result, error) {
	reqLogger := log.WithValues("Request.Namespace", request.Namespace, "Request.Name", request.Name)
	reqLogger.Info("Reconciling KrmRedis")

	// Fetch the KrmRedis instance
	cr := &krmv1.KrmRedis{}
	err := r.client.Get(context.TODO(), request.NamespacedName, cr)
	if err != nil {
		if errors.IsNotFound(err) {
			// Request object not found, could have been deleted after reconcile request.
			// Owned objects are automatically garbage collected. For additional cleanup logic use finalizers.
			// Return and don't requeue
			return reconcile.Result{}, nil
		}
		// Error reading the object - requeue the request.
		return reconcile.Result{}, err
	}

	pv, result, err := createRedisPersistentVolume(r, reqLogger, cr)
	if err != nil {
		return result, err
	}

	pvc, result, err := createRedisPersistentVolumeClaim(r, reqLogger, cr, pv)
	if err != nil {
		return result, err
	}

	deploy, result, err := createRedisDeployment(r, reqLogger, cr, pvc)
	if err != nil {
		return result, err
	}

	_, result, err = createRedisService(r, reqLogger, cr, deploy)
	if err != nil {
		return result, err
	}

	// All required resources successfully created
	return reconcile.Result{}, nil
}

// Creates Persistent Volume and blocks with an error if occurred
func createRedisPersistentVolume(r *ReconcileKrmRedis, reqLogger logr.Logger, cr *krmv1.KrmRedis) (*corev1.PersistentVolume, reconcile.Result, error) {
	pv := newRedisPersistentVolumeForCR(cr)
	// Set KrmRedis instance as the owner and controller
	if err := controllerutil.SetControllerReference(cr, pv, r.scheme); err != nil {
		return nil, reconcile.Result{}, err
	}

	existingPv := &corev1.PersistentVolume{}
	err := r.client.Get(context.TODO(), types.NamespacedName{Name: pv.Name}, existingPv)
	if err != nil && errors.IsNotFound(err) {
		reqLogger.Info("Creating new Persistent Volume", "PersistentVolume.Namespace", pv.Namespace, "PersistentVolume.Name", pv.Name)
		err = r.client.Create(context.TODO(), pv)
		if err != nil {
			return nil, reconcile.Result{}, err
		}
	} else if err != nil {
		return nil, reconcile.Result{}, err
	} else {
		// PV already exists
		if existingPv.Status.Phase != corev1.VolumeAvailable {
			reqLogger.Info("Existing Persistent Volume is not available", "PersistentVolume.Status.Phase", existingPv.Status.Phase)
			reqLogger.Info("Existing PV", "PV.ResourceVersion", existingPv.ResourceVersion)
			// Persistent Volume could still be terminating, try again later to see if it has been garbage collected
			wait := 15 * time.Second
			return nil, reconcile.Result{RequeueAfter: wait}, ctrlerrors.PersistentVolumeNotAvailable()
		}
	}

	return pv, reconcile.Result{}, nil
}

// Creates Persistent Volume Claim and blocks with an error if occurred
func createRedisPersistentVolumeClaim(r *ReconcileKrmRedis, reqLogger logr.Logger, cr *krmv1.KrmRedis, pv *corev1.PersistentVolume) (*corev1.PersistentVolumeClaim, reconcile.Result, error) {
	pvc := newRedisPersistentVolumeClaimForCR(cr, pv)
	// Set KrmRedis instance as the owner and controller
	if err := controllerutil.SetControllerReference(cr, pvc, r.scheme); err != nil {
		return nil, reconcile.Result{}, err
	}

	existingPvc := &corev1.PersistentVolumeClaim{}
	err := r.client.Get(context.TODO(), types.NamespacedName{Name: pvc.Name, Namespace: pvc.Namespace}, existingPvc)
	if err != nil && errors.IsNotFound(err) {
		reqLogger.Info("Creating new Persistent Volume Claim", "PersistentVolumeClaim.Namespace", pvc.Namespace, "PersistentVolumeClaim.Name", pvc.Name)
		err = r.client.Create(context.TODO(), pvc)
		if err != nil {
			return nil, reconcile.Result{}, err
		}
	} else if err != nil {
		return nil, reconcile.Result{}, err
	} else {
		// PVC already exists
		reqLogger.Info(
			"Skip creating PersistentVolumeClaim: PV already exists",
			"PersistentVolumeClaim.Namespace", existingPvc.Namespace,
			"PersistentVolumeClaim.Name", existingPvc.Name,
		)
		pvc = existingPvc
	}

	return pvc, reconcile.Result{}, nil
}

// Creates Deployment and blocks with an error if occurred
func createRedisDeployment(r *ReconcileKrmRedis, reqLogger logr.Logger, cr *krmv1.KrmRedis, pvc *corev1.PersistentVolumeClaim) (*extv1beta1.Deployment, reconcile.Result, error) {
	deploy := newRedisDeploymentForCR(cr, pvc)
	// Set KrmRedis instance as the owner and controller
	if err := controllerutil.SetControllerReference(cr, deploy, r.scheme); err != nil {
		return nil, reconcile.Result{}, err
	}

	existingDeploy := &extv1beta1.Deployment{}
	err := r.client.Get(context.TODO(), types.NamespacedName{Name: deploy.Name, Namespace: deploy.Namespace}, existingDeploy)
	if err != nil && errors.IsNotFound(err) {
		reqLogger.Info("Creating a new Deployment", "Deployment.Namespace", deploy.Namespace, "Deployment.Name", deploy.Name)
		err = r.client.Create(context.TODO(), deploy)
		if err != nil {
			return nil, reconcile.Result{}, err
		}
	} else if err != nil {
		return nil, reconcile.Result{}, err
	} else {
		reqLogger.Info(
			"Skip creating Deployment: Deployment already exists",
			"Deployment.Namespace", existingDeploy.Namespace,
			"Deployment.Name", existingDeploy.Name,
		)
		// Deployment already exists
		deploy = existingDeploy
	}

	return deploy, reconcile.Result{}, nil
}

// Creates Service and blocks with an error if occurred
func createRedisService(r *ReconcileKrmRedis, reqLogger logr.Logger, cr *krmv1.KrmRedis, deploy *extv1beta1.Deployment) (*corev1.Service, reconcile.Result, error) {
	service := newRedisServiceForCR(cr, deploy)
	// Set KrmRedis instance as the owner and controller
	if err := controllerutil.SetControllerReference(cr, service, r.scheme); err != nil {
		return nil, reconcile.Result{}, err
	}

	existingService := &corev1.Service{}
	err := r.client.Get(context.TODO(), types.NamespacedName{Name: service.Name, Namespace: service.Namespace}, existingService)
	if err != nil && errors.IsNotFound(err) {
		reqLogger.Info("Creating a new Service", "Service.Namespace", service.Namespace, "Service.Name", service.Name)
		err = r.client.Create(context.TODO(), service)
		if err != nil {
			return nil, reconcile.Result{}, err
		}
	} else if err != nil {
		return nil, reconcile.Result{}, err
	} else {
		// Service already exists
		reqLogger.Info(
			"Skip creating Service: PV already exists",
			"Service.Namespace", existingService.Namespace,
			"Service.Name", existingService.Name,
		)
		service = existingService
	}

	return service, reconcile.Result{}, nil
}

func newRedisPersistentVolumeForCR(cr *krmv1.KrmRedis) *corev1.PersistentVolume {
		labels := map[string]string{
			"instance": cr.Name,
		}

		return &corev1.PersistentVolume{
			ObjectMeta: metav1.ObjectMeta{
				Name: 			cr.Name,
				Namespace: 	cr.Namespace,
				Labels: 		labels,
			},
			Spec: corev1.PersistentVolumeSpec{
				Capacity: map[corev1.ResourceName]resource.Quantity{
					corev1.ResourceStorage: cr.Spec.StorageSpec.Storage,
				},
				AccessModes: cr.Spec.StorageSpec.AccessModes,
				PersistentVolumeReclaimPolicy: corev1.PersistentVolumeReclaimRetain,
				PersistentVolumeSource: corev1.PersistentVolumeSource{
					HostPath: &cr.Spec.StorageSpec.HostPath,
				},
			},
		}
}

func newRedisPersistentVolumeClaimForCR(cr *krmv1.KrmRedis, pv *corev1.PersistentVolume) *corev1.PersistentVolumeClaim {
	labels := map[string]string{
		"app.kubernetes.io/name": cr.Name,
	}

	return &corev1.PersistentVolumeClaim{
		ObjectMeta: metav1.ObjectMeta{
			Name: 			cr.Name,
			Namespace:	cr.Namespace,
			Labels: 		labels,
		},
		Spec: corev1.PersistentVolumeClaimSpec{
			AccessModes: cr.Spec.StorageSpec.AccessModes,
			Selector: &metav1.LabelSelector{
				MatchLabels: pv.Labels,
			},
			Resources: corev1.ResourceRequirements{
				Requests: pv.Spec.Capacity,
			},
		},
	}
}

func newRedisDeploymentForCR(cr *krmv1.KrmRedis, pvc *corev1.PersistentVolumeClaim) *extv1beta1.Deployment {
	labels := map[string]string{
		"app.kubernetes.io/name": cr.Name,
	}

	return &extv1beta1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name: 			cr.Name,
			Namespace: 	cr.Namespace,
			Labels: 		labels,
		},
		Spec: extv1beta1.DeploymentSpec{
			Selector: &metav1.LabelSelector{
				MatchLabels: labels,
			},
			Strategy: extv1beta1.DeploymentStrategy{
				Type: extv1beta1.RecreateDeploymentStrategyType,
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Namespace: 	cr.Namespace,
					Labels: 		labels,
				},
				Spec: corev1.PodSpec{
					NodeSelector: cr.Spec.NodeSelector,
					Containers: []corev1.Container{
						{
							Name: cr.Name,
							Image: "frodenas/redis",
							ImagePullPolicy: corev1.PullAlways,
							EnvFrom: []corev1.EnvFromSource{
								{
									SecretRef: &corev1.SecretEnvSource{
										LocalObjectReference: corev1.LocalObjectReference{
											Name: "krm-redis",
										},
									},
								},
							},
							Ports: []corev1.ContainerPort{
								{
									Name: "http",
									ContainerPort: 6379,
									Protocol: corev1.ProtocolTCP,
								},
							},
							VolumeMounts: []corev1.VolumeMount{
								{
									Name: cr.Name,
									MountPath: "/data",
								},
							},
						},
					},
					Volumes: []corev1.Volume{
						{
							Name: cr.Name,
							VolumeSource: corev1.VolumeSource{
								PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{
									ClaimName: pvc.Name,
								},
							},
						},
					},
				},
			},
		},
	}
}

func newRedisServiceForCR(cr *krmv1.KrmRedis, deploy *extv1beta1.Deployment) *corev1.Service {
	labels := map[string]string{
		"app.kubernetes.io/name": cr.Name,
	}

	return &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{
			Name: 			cr.Name,
			Namespace: 	cr.Namespace,
			Labels: 		labels,
		},
		Spec: corev1.ServiceSpec{
			Type: corev1.ServiceTypeClusterIP,
			Ports: []corev1.ServicePort{
				{
					Port: 6379,
				},
			},
			Selector: deploy.Spec.Template.Labels,
		},
	}
}
