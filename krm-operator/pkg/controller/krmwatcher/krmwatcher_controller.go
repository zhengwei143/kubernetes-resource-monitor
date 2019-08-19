package krmwatcher

import (
	"fmt"
	"context"
	"strconv"

	krmv1 "github.com/zhengwei143/kubernetes-resource-monitor/krm-operator/pkg/apis/krm/v1"
	corev1 "k8s.io/api/core/v1"
	extv1beta1 "k8s.io/api/extensions/v1beta1"
	"k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
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

var log = logf.Log.WithName("controller_krmwatcher")

/**7
* USER ACTION REQUIRED: This is a scaffold file intended for the user to modify with their own Controller
* business logic.  Delete these comments after modifying this file.*
 */

// Add creates a new KrmWatcher Controller and adds it to the Manager. The Manager will set fields on the Controller
// and Start it when the Manager is Started.
func Add(mgr manager.Manager) error {
	return add(mgr, newReconciler(mgr))
}

// newReconciler returns a new reconcile.Reconciler
func newReconciler(mgr manager.Manager) reconcile.Reconciler {
	return &ReconcileKrmWatcher{client: mgr.GetClient(), scheme: mgr.GetScheme()}
}

// add adds a new Controller to mgr with r as the reconcile.Reconciler
func add(mgr manager.Manager, r reconcile.Reconciler) error {
	// Create a new controller
	c, err := controller.New("krmwatcher-controller", mgr, controller.Options{Reconciler: r})
	if err != nil {
		return err
	}

	// Watch for changes to primary resource KrmWatcher
	err = c.Watch(&source.Kind{Type: &krmv1.KrmWatcher{}}, &handler.EnqueueRequestForObject{})
	if err != nil {
		return err
	}

	// TODO(user): Modify this to be the types you create that are owned by the primary resource
	// Watch for changes to secondary resource Pods and requeue the owner KrmWatcher
	// err = c.Watch(&source.Kind{Type: &corev1.Pod{}}, &handler.EnqueueRequestForOwner{
	// 	IsController: true,
	// 	OwnerType:    &krmv1.KrmWatcher{},
	// })
	err = c.Watch(&source.Kind{Type: &extv1beta1.Deployment{}}, &handler.EnqueueRequestForOwner{
		IsController: true,
		OwnerType:    &krmv1.KrmWatcher{},
	})

	if err != nil {
		return err
	}

	return nil
}

// blank assignment to verify that ReconcileKrmWatcher implements reconcile.Reconciler
var _ reconcile.Reconciler = &ReconcileKrmWatcher{}

// ReconcileKrmWatcher reconciles a KrmWatcher object
type ReconcileKrmWatcher struct {
	// This client, initialized using mgr.Client() above, is a split client
	// that reads objects from the cache and writes to the apiserver
	client client.Client
	scheme *runtime.Scheme
}

// Reconcile reads that state of the cluster for a KrmWatcher object and makes changes based on the state read
// and what is in the KrmWatcher.Spec
// TODO(user): Modify this Reconcile function to implement your Controller logic.  This example creates
// a Pod as an example
// Note:
// The Controller will requeue the Request to be processed again if the returned error is non-nil or
// Result.Requeue is true, otherwise upon completion it will remove the work from the queue.
func (r *ReconcileKrmWatcher) Reconcile(request reconcile.Request) (reconcile.Result, error) {
	reqLogger := log.WithValues("Request.Namespace", request.Namespace, "Request.Name", request.Name)
	reqLogger.Info("Reconciling KrmWatcher")

	// Fetch the KrmWatcher instance
	instance := &krmv1.KrmWatcher{}
	err := r.client.Get(context.TODO(), request.NamespacedName, instance)
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

	// Define a new Pod object
	// pod := newPodForCR(instance)
	deployment := newDeploymentForCR(instance)

	// Set KrmWatcher instance as the owner and controller
	if err := controllerutil.SetControllerReference(instance, deployment, r.scheme); err != nil {
		return reconcile.Result{}, err
	}

	// Check if this Pod already exists
	found := &extv1beta1.Deployment{}
	err = r.client.Get(context.TODO(), types.NamespacedName{Name: deployment.Name, Namespace: deployment.Namespace}, found)
	if err != nil && errors.IsNotFound(err) {
		reqLogger.Info("Creating a new Deployment", "Deployment.Namespace", deployment.Namespace, "Deployment.Name", deployment.Name)
		err = r.client.Create(context.TODO(), deployment)
		if err != nil {
			return reconcile.Result{}, err
		}

		// Pod created successfully - don't requeue
		return reconcile.Result{}, nil
	} else if err != nil {
		return reconcile.Result{}, err
	}

	// Pod already exists - don't requeue
	reqLogger.Info("Skip reconcile: Deployment already exists", "Deployment.Namespace", found.Namespace, "Deployment.Name", found.Name)
	return reconcile.Result{}, nil
}

// newPodForCR returns a busybox pod with the same name/namespace as the cr
func newPodForCR(cr *krmv1.KrmWatcher) *corev1.Pod {
	labels := map[string]string{
		"app": cr.Name,
	}
	return &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{
			Name:      cr.Name + "-pod",
			Namespace: cr.Namespace,
			Labels:    labels,
		},
		Spec: corev1.PodSpec{
			Containers: []corev1.Container{
				{
					Name:    "busybox",
					Image:   "busybox",
					Command: []string{"sleep", "3600"},
				},
			},
		},
	}
}

func newDeploymentForCR(cr *krmv1.KrmWatcher) *extv1beta1.Deployment {
	deploymentName := "krm-" + cr.Spec.WatchingResource + "-watcher-v2"
	labels := map[string]string{
		"app.kubernetes.io/name": deploymentName,
	}
	redisService := "krm-redis.kube-system.svc.cluster.local"
	initContainer := corev1.Container{
		Name: 		"init-watcher",
		Image: 		"busybox:1.28",
		Command: 	[]string{
			"sh",
			"-c",
			fmt.Sprintf(
				"until nslookup %s; do echo waiting for %s; sleep 2; done;",
				redisService,
				redisService,
			),
		},
	}

	return &extv1beta1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name: 			deploymentName,
			Namespace: 	cr.Spec.Namespace,
			Labels: 		labels,
		},
		Spec: extv1beta1.DeploymentSpec{
			Selector: &metav1.LabelSelector{
				MatchLabels: labels,
			},
			Strategy: extv1beta1.DeploymentStrategy{
				Type: "Recreate",
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Namespace: 	cr.Namespace,
					Labels: 		labels,
				},
				Spec: corev1.PodSpec{
					ServiceAccountName: "krm-operator",
					// NOTE: Only to be used on dev cluster
					NodeSelector: map[string]string{
						"kubernetes.io/hostname": "sgw0008",
					},
					InitContainers: []corev1.Container{ initContainer },
					Containers: []corev1.Container{
						newWatcherContainer(cr, "streamer"),
						newWatcherContainer(cr, "verifier"),
						newWatcherContainer(cr, "aggregator"),
					},
				},
			},
		},
	}
}

func newWatcherContainer(cr *krmv1.KrmWatcher, app string) corev1.Container {
	appArgs := map[string][]string{
		"streamer": 	[]string{ "app_streamer.py" },
		"verifier": 	[]string{ "app_verifier.py" },
		"aggregator": []string{ "app_aggregator.py" },
	}

	return corev1.Container{
		Name: app,
		Image: cr.Spec.AppImage,
		ImagePullPolicy: "Always",
		EnvFrom: []corev1.EnvFromSource{
			{
				SecretRef: &corev1.SecretEnvSource{
					LocalObjectReference: corev1.LocalObjectReference{
						Name: "krm-redis",
					},
				},
			},
			{
				SecretRef: &corev1.SecretEnvSource{
					LocalObjectReference: corev1.LocalObjectReference{
						Name: "cluster",
					},
				},
			},
		},
		Env: []corev1.EnvVar{
			{
				Name: "API_RESOURCE",
				Value: cr.Spec.WatchingResource,
			},
			{
				Name: "VERIFICATION_WAIT_DURATION",
				Value: strconv.FormatInt(cr.Spec.VerificationWaitDuration, 10),
			},
			{
				Name: "AGGREGATION_WAIT_DURATION",
				Value: strconv.FormatInt(cr.Spec.AggregationWaitDuration, 10),
			},
		},
		Command: []string{ "python3.6" },
		Args: appArgs[app],
	}
}
