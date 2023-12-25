let scene, camera, renderer;
let spheres = [];
let universe, universe2, universe3;

init();
animate();

function init() {
    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 0, 100); // Adjusted camera position

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    function createMesh(geometry, texturePath, rotationX, side) {
        const texture = new THREE.TextureLoader().load(texturePath);
        const material = new THREE.MeshPhongMaterial({
            map: texture,
            side: side,
            shininess: 100,
            specular: new THREE.Color('grey'),
            bumpMap: texture,
            bumpScale: 0.5
        });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.rotation.x = rotationX;
        return mesh;
    }

    const universeGeometry = new THREE.BoxGeometry(100, 100, 100);
    universe = createMesh(universeGeometry, '/static/textures/jumbo.jpg', Math.PI / 3, THREE.BackSide);

    const universeGeometry2 = new THREE.BoxGeometry(100, 100, 100);
    universe2 = createMesh(universeGeometry2, '/static/textures/intro.jpg', Math.PI / 1, THREE.BackSide);

    const universeGeometry3 = new THREE.BoxGeometry(100, 100, 100);
    universe3 = createMesh(universeGeometry3, '/static/textures/library.jpg', Math.PI / 20, THREE.BackSide);

    scene.add(universe);
    scene.add(universe2);
    scene.add(universe3);

    const geometry = new THREE.SphereGeometry(1, 32, 32);
    const material = new THREE.MeshBasicMaterial({ color: 0xFFA500 }); // Changed color to orange

    let texture = new THREE.TextureLoader().load('/static/images/energy.jpg');
    material.map = texture;

    const bgTexture = new THREE.TextureLoader().load('/static/images/avalon.jpg');
    scene.background = bgTexture;

    for (let i = 0; i < 100; i++) {
        let sphere = new THREE.Mesh(geometry, material);
        sphere.position.x = Math.random() * 10 - 5;
        sphere.position.y = Math.random() * 10 - 5;
        sphere.scale.set(4, 20, 4);
        sphere.position.z = Math.random() * 10 - 5;
        sphere.velocity = new THREE.Vector3(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5);
        spheres.push(sphere);
        scene.add(sphere);

        // Add click event listener to stop object movement
        sphere.isMoving = true; // A custom property to track movement
    // Use this code to add click event listener using addEventListener
    sphere.addEventListener('click', function (event) {
        if (this.isMoving) {
            this.isMoving = false;
            this.velocity.set(0, 0, 0);
        } else {
            this.isMoving = true;
            this.velocity = new THREE.Vector3(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5);
        }
    });
    }

    const fontLoader = new THREE.FontLoader();
    fontLoader.load('/path/to/wdmmorpg.json', function (font) {
        const textGeometry = new THREE.TextGeometry('wdmmorpg', {
            font: font,
            size: 2, // Adjust the size as needed
            height: 0.2, // Adjust the height as needed
        });

        const textMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });

        const textMesh = new THREE.Mesh(textGeometry, textMaterial);
        textMesh.position.set(-10, 10, 0); // Adjust the position as needed
        scene.add(textMesh);
    });

    animate(); // Start the animation loop
}

function animate() {
    requestAnimationFrame(animate);

    // Rotation and movement for universe objects
    universe.rotation.x += 0.001;

    spheres.forEach(sphere => {
        if (sphere.isMoving) {
            sphere.position.add(sphere.velocity);

            if (Math.abs(sphere.position.x) > 50) sphere.velocity.x *= -0.01;
            if (Math.abs(sphere.position.y) > 50) sphere.velocity.y *= -0.02;
            if (Math.abs(sphere.position.z) > 50) sphere.velocity.z *= -0.2;
        }
    });

    // Rotation and movement for other objects in the scene
    scene.children.forEach(child => {
        if (child instanceof THREE.Mesh) {
            child.rotation.x += 0.01;
            child.rotation.y += 0.02;
            child.rotation.z += 0;

            child.position.x += Math.random() > 1.5 ? 0.02 : -0.01;
            child.position.y += Math.random() > 1.5 ? 0.02 : 0.2;
            child.position.z += Math.random() > 0.0 ? -0.12 : 0.2;
        }
    });

    renderer.render(scene, camera);
}
