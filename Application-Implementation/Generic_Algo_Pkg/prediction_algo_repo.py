from Generic_Algo_Pkg import mylr as ml
from Generic_Algo_Pkg import mysvm as ms
from custom_algo_pkg import slide_algo as sa


def surge_svm(location,time,type='uber'):
    surge = ms.svm_predict(location,time,type)
    return surge

def surge_lr(location,time,type='uber'):
    surge = ml.lr_predict(location,time,type)
    return surge

def surge_slide(location,time,type='uber'):
    surge = sa.predict(location,time,type)
    #tmp = kmeans_predict(location,time,type)
    return surge