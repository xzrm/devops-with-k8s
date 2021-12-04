import axios from 'axios'
import Config  from '../config.json'

// const baseUrl = process.env.REACT_APP_BACKEND_BASE_URL
const baseUrl = Config.BACKEND_BASE_URL

const getAll = async () => {
    const response = await axios.get(baseUrl)
    return response.data
}

const create = async newObject => {
    const response = await axios.post(baseUrl, newObject)
    return response.data
}

const update = async (id, newObject) => {
    const response = await axios.put(`${baseUrl}/${id}`, newObject)
    return response.data
}

const remove = async (id) => {
    return axios.delete(`${baseUrl}/${id}`)
}

export default { getAll, create, update, remove }