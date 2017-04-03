function checkStatus(response) {
    if (response.status >= 200 && response.status < 300) {
        return response;
    }
    const error = new Error(`HTTP Error ${response.statusText}`);
    error.status = response.statusText;
    error.response = response;
    console.log(error);
    throw error;
}

function parseJSON(response) {
    return response.json();
}


export const dummyMapData = () => {
	const dummyMapUrl = 'https://jamesleondufour.carto.com/api/v2/sql?q=select%20count,%20long,%20lat,%20date%20from%20public.gdelt_refugee_2016';
	const dummyTestUrl = `${window.location.orgin}/api/test`;
	return fetch(dummyTestUrl).then(checkStatus).then(parseJSON)
	// return fetch(dummyMapUrl).then(response => {
	// 		return response.json();
	// 	}
	// )
}