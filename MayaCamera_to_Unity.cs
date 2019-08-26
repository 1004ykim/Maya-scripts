using UnityEngine;
using System.Collections;

public class camController : MonoBehaviour
{
    public Camera MainCam;
    public GameObject camMove;
    public Transform Target;



    void LateUpdate()
    {
        transform.position = camMove.transform.position;
       transform.LookAt(Target);
//       MainCam.nearClipPlane = camMove.transform.localScale.x;
//       MainCam.farClipPlane = camMove.transform.localScale.y;
       MainCam.fieldOfView = camMove.transform.localScale.z - 2;


    }

}
