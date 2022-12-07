
varying float2 Tex;

void main()
{
	gl_FragColor = FinalScenePassPS(true, 0, false, Tex);
}
